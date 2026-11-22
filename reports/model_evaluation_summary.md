# Model Evaluation Summary

## Objective
The purpose of model evaluation was to assess the performance of Content-Based Filtering and User-Based Collaborative Filtering using a training and testing dataset split.

## Evaluation Metrics
- Precision@10
- Recall@10
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)

## Results

| Metric | Content-Based | Collaborative |
|---|---:|---:|
| Precision@10 | 0.025441 | 0.018823 |
| Recall@10 | 0.018781 | 0.011822 |
| RMSE | N/A | 0.894543 |
| MAE | N/A | 0.696043 |

## Interpretation
Content-Based Filtering achieved higher Precision@10 and Recall@10 than Collaborative Filtering in the current evaluation.

Collaborative Filtering achieved an RMSE of 0.894543 and an MAE of 0.696043 for rating prediction.

The results indicate that both approaches provide useful but limited recommendation performance under the current experimental setup. Further improvements may include hybrid recommendation techniques, improved similarity calculations, and more comprehensive evaluation.

## Limitations
The ranking evaluation uses movies available in the training rating matrix as candidates. Content-Based Filtering and Collaborative Filtering currently use different candidate catalogs. Therefore, their ranking results should be interpreted cautiously and are not a fully controlled comparison.