import numpy as np
import matplotlib.pyplot as plt

rnd = np.random.default_rng()

density = np.array(
    [.02, .026, .023, .017, .022, .019, .018, .018, .017, .022])

n_density = len(density)

n_trials = 10_000
results = np.zeros(n_trials)

for i in range(n_trials):
    fake_density = rnd.choice(density, size=n_density)
    results[i] = np.mean(fake_density)

plt.hist(results, bins=25)
plt.title('Bootstrap distribution of density means')
plt.xlabel('Bootstrap density means')

mean_limits = np.quantile(results, [0.025, 0.975])

print('95% percent limits for mean:', mean_limits)
