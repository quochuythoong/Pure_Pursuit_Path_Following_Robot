import matplotlib.pyplot as plt
import numpy as np

# Parameters for normal distribution
mean = 10  # Mean time in minutes
std_dev = 2.8  # Smaller standard deviation for a more bell-shaped curve
num_people = 400  # Number of people

# Generate data using normal distribution
times = np.random.normal(mean, std_dev, num_people)

# Ensure all times are within the 0-20 minute range
times = np.clip(times, 0, 20)
print("Generated times (minutes):")
print(times)
# Create the histogram
plt.figure(figsize=(10, 6))
plt.hist(times, bins=np.arange(0, 22, 1), color='skyblue', edgecolor='black', alpha=0.7)

# Add titles and labels
plt.title("Time Taken by 400 People to Find a Bike Parking Slot", fontsize=14)
plt.xlabel("Time (minutes)", fontsize=12)
plt.ylabel("Number of People", fontsize=12)
plt.xticks(np.arange(0, 21, 1))
plt.grid(axis='y', alpha=0.75)

# Show the plot
plt.tight_layout()
plt.show()
