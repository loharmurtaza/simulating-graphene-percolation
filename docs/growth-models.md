# Growth models and fitting

The simulation does not model growth chemistry directly. It fits a smooth curve S(t) to the measured coverage and then forces the simulated flakes to follow that curve. All model functions live in `utils/math.py`. Coverage values are in **percent** throughout.

Fitting uses `scipy.optimize.curve_fit`. With `USE_STD=True`, the experimental standard deviations are passed as `sigma` with `absolute_sigma=True`, so points with smaller uncertainty carry more weight and the covariance `pcov` is in absolute units.

## Logistic model (`--model logistic`)

$$
S(t) = \frac{L}{1 + e^{-k(t - t_0)}}
$$

| Parameter | Meaning | Initial guess |
|-----------|---------|---------------|
| `L` | Saturation coverage (%) | 100 |
| `k` | Growth rate (1/min) | 0.1 |
| `t0` | Inflection (midpoint) time, min | 5.0 |

Derivative:

$$
\frac{dS}{dt} = \frac{L\,k\,e^{-k(t-t_0)}}{\left(1 + e^{-k(t-t_0)}\right)^2}
$$

Functions: `logistic`, `logistic_derivative`, `fit_surface_coverage_logistic` (unbounded fit).

The logistic curve is never exactly 0, so S(0) > 0 and the simulation starts with a small non-zero coverage.

## Exponential model (`--model exponential`)

This is the autocatalytic model from the paper:

$$
\theta_G(t) = \left(\frac{e^{\alpha t + C_1} - 1}{e^{\alpha t + C_1} + 1}\right)^2 \times 100
= 100\,\tanh^2\!\left(\frac{\alpha t + C_1}{2}\right)
$$

| Parameter | Meaning | Initial guess | Bounds (with `USE_STD`) |
|-----------|---------|---------------|-------------------------|
| `alpha` | Growth rate (1/min) | 0.3 | [0.01, 2] |
| `C1` | Offset constant | −0.5 | [−5, 5] |

- θ_G = 0 at $t_{min} = -C_1/\alpha$. The exponential pipelines start their time grid there, so the simulation begins from zero coverage.
- The exponent $\alpha t + C_1$ is clipped to [−50, 50] to avoid overflow.
- Bounds and `maxfev=5000` apply only to the weighted fit (`USE_STD=True`). The unweighted fit is unbounded.

Derivative (chain rule, $x = \alpha t + C_1$):

$$
\frac{d\theta_G}{dt} = 2\,\frac{e^x - 1}{e^x + 1}\cdot\frac{2e^x}{(e^x+1)^2}\cdot\alpha \times 100
$$

The inflection point (fastest growth) is the maximum of the derivative. The surface pipeline finds it with `argmax` over the time grid. `find_inflection_point()` does the same with `scipy.optimize.minimize_scalar` over [0, 30] min, but no pipeline currently calls it.

Functions: `exponential_function`, `exponential_function_derivative`, `fit_surface_coverage_exponential`, `find_inflection_point`.

## tanh² model (exploratory)

$$
S(t) = A\,\tanh^2\big(k(t - t_0)\big) + B
$$

Used only by `scripts/test_scripts/test_tanh_squared.py`. It has four parameters, but the default `p0=[0.5]` gives only one starting value, so `curve_fit` will fail unless you pass a full `p0` (for example `[100, 0.2, 0, 0]`). Functions: `tanh_squared`, `tanh_squared_derivative`, `fit_surface_coverage_tanh_squared`.

## Mean-area extrapolation

`estimate_mean_areas_from_coverage()` fits a straight line through `(coverage, mean flake area)` pairs and evaluates it at the experimental coverages. The surface pipelines use it with two measured samples and only log the result. It does not affect the simulation.
