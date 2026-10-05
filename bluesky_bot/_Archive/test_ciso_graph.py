import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
title = "CISO thought he had a 'r3@lg00dp@$$w0rd' but forgot to patch"
safe_title = title.replace('$', r'\$')
ax.set_title(safe_title)
plt.tight_layout()
print("ESCAPED DOLLAR SUCCESS!")
