# Loading library packages
library(dplyr)
library(ggplot2)
library(reshape2)

# Loading the dataset for task 1
PATH <- "~/Downloads/Evaluation_HCI_project - Task3.csv"

# Reading the dataset file
df <- read.csv(PATH) %>%
  mutate(Interface = factor(Interface, ordered = TRUE)) %>%
  mutate(User = factor(User, ordered=TRUE))

# Data for reference
print(glimpse(df))
print(levels(df$Interface))

# Printing the different statistical measures of data
print(summary(df))

# Plotting BoxPlot to visualize the different statistical measures
ggplot(df, aes(x=Interface, y=Time, fill=Interface)) +
  geom_boxplot() +
  geom_jitter(shape=20,
              color="red",
              position=position_jitter(0.21)) +
  theme_light()

# Performing ANOVA test for within-subject design
anova_one_way <- aov(Time~Interface+Error(User/Interface), data=df)
# Print summary of ANOVA test results
print(summary(anova_one_way))

# Performing Pairwise t-test without adjustment
ttest <- pairwise.t.test(df$Time, df$Interface, p.adj="none")
print(ttest[3])

# Plot a heat-map for visualization of p-values
melted_ttest <- melt(ttest[3])
print(melted_ttest)
ggplot(data = melted_ttest, aes(x=Var1, y=Var2, fill=value)) +
  geom_tile(color="white")+
  scale_fill_gradient2(low = "lightblue", high = "darkblue", mid = "blue",
                       midpoint = 0.5, limit = c(0,1), space = "Lab",
                       name="p value") +
  theme_minimal()+
  theme(axis.text.x = element_text(angle = 0, vjust = 1, hjust = 1))+
  coord_fixed()

