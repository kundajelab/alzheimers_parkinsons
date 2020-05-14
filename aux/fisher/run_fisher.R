## Prepare a two-dimensional contingency table
contingency.table <- data.frame(matrix(nrow=2, ncol=2))
rownames(contingency.table) <- c("specific", "non.specific")
colnames(contingency.table) <- c("cicero", "no.cicero")

## Assign the values one by one to make sure we put them in the right
## place (this is not necessary, we could enter the 4 values in a
## single instruction).
contingency.table["specific", "cicero"] <- 210008 ## Number of marked genes in the selection
contingency.table["specific", "no.cicero"] <- 11053 ## Number of non-marked genes in the selection
contingency.table["non.specific", "cicero"] <- 108988 ## Number of marked genes outside of the selection
contingency.table["non.specific", "no.cicero"] <- 28972 ## Number of non-marked genes in the selection


print(contingency.table)

## Run Fisher's exact test
ftest.result <- fisher.test(x=contingency.table)
print(ftest.result)