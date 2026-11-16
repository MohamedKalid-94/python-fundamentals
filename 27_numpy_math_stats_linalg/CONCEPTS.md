# Module 27: NumPy Math, Statistics, Random Numbers and Linear Algebra, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Trigonometric | Functions | `sin cos tan`, `arcsin arccos arctan`, `arctan2(y, x)` (all four quadrants), `hypot`, `unwrap`; angles in radians (`radians`, `degrees`) |
| 01 | Trigonometric | Floats | `np.sin(np.pi)` is not 0: compare with `np.isclose` |
| 01 | Hyperbolic | Functions | `sinh cosh tanh` and their inverses; `tanh` squashes into (-1, 1); `cosh² - sinh² = 1` |
| 02 | Exponential | Functions | `exp`, `exp2`, `expm1` (accurate for tiny x), `power`, `sqrt`, `cbrt`, `square` |
| 02 | Logarithmic | Functions | `log`, `log10`, `log2`, `log1p`, `logaddexp`; `log(0)` is `-inf`, `log(-1)` is `nan` |
| 02 | Stability | Softmax | Subtract the maximum before `exp`, or `exp(1000)` overflows to `nan` |
| 02 | Rounding | Functions | `round` (half to even), `floor`, `ceil`, `trunc`, `rint`, `modf`; `np.round(2.675, 2)` is 2.68 but Python's `round` gives 2.67 |
| 03 | ufunc | Idea | A compiled function with broadcasting, `out=`, `where=`, `dtype=`; `nin`, `nout`, `types` |
| 03 | ufunc | Methods | `reduce`, `accumulate`, `outer`, `at` (repeats count), `reduceat` |
| 03 | ufunc | Creating | `np.vectorize` (a Python loop in disguise), `np.frompyfunc` (object arrays); prefer real ufuncs such as `np.minimum` |
| 04 | Arithmetic ufuncs | Group | `add subtract multiply divide power mod absolute negative reciprocal` |
| 04 | Summation | Functions | `sum`, `cumsum`, `add.reduce`; small integer types are summed in a wider type; `math.fsum` for exact float sums |
| 04 | Product | Functions | `prod`, `cumprod`; `int64` overflows at 21! |
| 04 | Difference | Functions | `diff` (`n=`, `axis=`, `prepend=`), `ediff1d`, `gradient` |
| 04 | LCM and GCD | Functions | `np.lcm`, `np.gcd`, and `.reduce` for a whole array |
| 04 | Set operations | Masks | A set as a boolean mask: `logical_and/or/xor/not`, `&`, `\|`, `^`, `~`; `unique`, `union1d` are functions, not ufuncs |
| 05 | Aggregates | Basics | `sum mean median min max argmin argmax ptp` with `axis`, `keepdims`, `dtype`, `where`, `initial` |
| 05 | Aggregates | Missing data | Plain functions return `nan`; `nansum nanmean nanmedian nanmin nanmax` skip it |
| 05 | Aggregates | Choice | The mean follows outliers, the median does not; `np.maximum` is element by element, `max` is a reduction |
| 06 | Statistics | Spread | `var`, `std` with `ddof=0` (population) or `ddof=1` (sample), `ptp`, IQR = Q3 - Q1 |
| 06 | Statistics | Position | `percentile` (0 to 100), `quantile` (0 to 1), `method=` for the interpolation |
| 06 | Statistics | Others | `average(weights=)`, mode with `unique(return_counts=True)`, `histogram`, `digitize`, `cov`, `corrcoef` |
| 06 | Statistics | Patterns | z-score, moving average with `convolve(mode="valid")`, running mean with `cumsum` |
| 07 | Random | Generator | `rng = np.random.default_rng(seed)`; the same seed gives the same numbers; always seed experiments and tests |
| 07 | Random | Methods | `random`, `integers` (high excluded), `choice(replace, p)`, `shuffle` (in place), `permutation` (copy), `permuted` |
| 07 | Random | Practice | Reproducible train/test split with a permutation; `SeedSequence.spawn` for independent streams; `RandomState` is legacy |
| 08 | Distributions | List | `uniform normal binomial poisson exponential rayleigh logistic pareto chisquare zipf multinomial`: parameters, mean and typical use |
| 08 | Distributions | Checks | Large samples have means close to theory; NumPy's `pareto` is the Lomax form; `size` can be a shape |
| 09 | Matrix operations | Products | `+ -` and `*` are element by element; `@`, `np.matmul`, `np.dot` is the matrix product; `(n,k) @ (k,m) -> (n,m)`; not commutative |
| 09 | Matrix operations | Others | `outer`, `inner`, `vdot`, `cross`, `trace`, `matrix_power`, `einsum`, `tensordot`, batched `matmul` |
| 09 | Matrix library | Legacy | `np.matrix` makes `*` a matrix product and is pending removal: use arrays and `@` |
| 10 | Linear algebra | Inverse and determinant | `inv`, `det`, `matrix_rank`, `cond`, `pinv`; a singular matrix raises `LinAlgError` |
| 10 | Linear algebra | Equations | `solve(A, b)` is better than `inv(A) @ b`; `lstsq` for the best fit |
| 10 | Linear algebra | Eigen | `eig`, `eigvals`, `eigh` (symmetric, sorted); check `A v = λ v`; vectors are defined up to a sign |
| 10 | Linear algebra | SVD | `U, s, Vt = svd(M, full_matrices=False)`; `U * s @ Vt` rebuilds `M`; the error of a rank-k approximation is the next singular value |
| 10 | Linear algebra | Norms | `norm(x, ord)`: 1, 2, `inf`, `"fro"`, `"nuc"` |
| 11 | Polynomials | Class | `Polynomial([c0, c1, ...])` (low to high), `p(x)`, `roots`, `fromroots`, `deriv`, `integ`, arithmetic, `divmod` |
| 11 | Polynomials | Fitting | `Polynomial.fit(x, y, deg).convert()`; the old `polyfit`, `poly1d`, `polyval` use high to low order |
| 12 | Worked examples | Patterns | IQR outliers, moving average, Monte Carlo, regression with R², softmax and loss, PCA with SVD, mesh currents with `solve`, quantisation error |