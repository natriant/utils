import pandas as pd
import matplotlib.pyplot as plt

# Load data, type: pandas
data = pd.read_csv("filename.csv")

# Plot for comparison
plt.figure(figsize=(12,8))
ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()
# Find best fit distribution
best_distribution, best_fit_name, best_fit_params = best_fit_distribution(data, 200, ax)
best_dist = getattr(st, best_fit_name)

print('The best fit is a {} distribution'.format(best_fit_name))

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={}'.format(k,v) for k,v in zip(param_names, best_fit_params)])

print('param_names',param_names)
print('param_Strings', param_str)


# Compute the mean and the variance of the distribution
if best_fit_name == 'expon':
    mean, var = best_distribution.stats(loc=best_fit_params[0], scale=best_fit_params[1], moments='mv')
elif best_fit_name == 'gamma':
    mean, var = best_distribution.stats(best_fit_params[0], loc=best_fit_params[1], scale=best_fit_params[2], moments='mv')
elif best_fit_name =='beta':
     mean, var = best_distribution.stats(best_fit_params[0], best_fit_params[1], loc=best_fit_params[2], scale=best_fit_params[3], moments='mv')
else:
    print('computing the mean and variance of this distibution is not yet implemented')

print('mu={}, var={}, simga={}'.format(mean, var, np.sqrt(var)))

# Update plots
# Update plots
ax.set_ylim(dataYLim)

# Make PDF with best params
pdf = make_pdf(best_dist, best_fit_params)

# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:.3f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax.set_title('Best fit distribution \n {} \n mean={:.3f}, sigma={:.5f}'.format(dist_str, mean, np.sqrt(var) ))


ax.set_xlabel('Betatron tune')
ax.set_ylabel(r'$\rho (\nu_b)$')
plt.savefig('study_name.png')
plt.show()
