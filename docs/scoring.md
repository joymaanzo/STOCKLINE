# Opportunity Score

The opportunity score is a deterministic heuristic implemented in `app/scoring.py` and `app/indicators.py`. It is calculated from three percentage inputs.

## Inputs

For at least 20 closing prices:

1. **20-day momentum**

   ```text
   momentum = (latest_close - prices[-20]) / prices[-20] * 100
   ```

   In this implementation, `prices[-20]` is the first price in the latest 20-price window. This is the implementation of the issue's "20-day momentum" wording; it is not a comparison with only the immediately preceding close. A zero base cannot produce a score.

2. **Position versus the 20-day SMA**

   ```text
   sma20 = sum(latest 20 closes) / 20
   position = (latest_close - sma20) / sma20 * 100
   ```

3. **5-day versus 20-day SMA trend**

   ```text
   sma5 = sum(latest 5 closes) / 5
   trend = (sma5 - sma20) / sma20 * 100
   ```

## Normalisation and score

Each percentage input is converted to a 0-100 component using the exact implementation formula:

```text
component = clamp(50 + percent * 5, 0, 100)
```

The scale of 5 was chosen so a 10% positive input reaches 100 and a 10% negative input reaches 0. It keeps a zero percentage centred at 50, makes the three inputs comparable, and deliberately saturates larger movements instead of allowing one input to dominate without limit.

The final score uses these weights:

```text
score = 0.40 * momentum_component
      + 0.40 * position_component
      + 0.20 * trend_component
```

The result is rounded to two decimal places.

## Labels

| Score | Label |
| --- | --- |
| 70-100 | Strong indicators |
| 40-69 | Watch |
| 0-39 | Weak indicators |

## Missing data

Fewer than 20 prices returns:

```text
Insufficient data to score
```

The response contains no numeric score. Missing or unusable indicator values, such as a zero denominator, use the same result.

## Worked example: down case

Use the 20 prices `[100] * 19 + [90]`.

1. **20-day SMA**

   ```text
   sma20 = (19 * 100 + 90) / 20
         = 1990 / 20
         = 99.5
   ```

2. **20-day momentum**

   ```text
   momentum = (90 - 100) / 100 * 100
            = -10%
   ```

3. **Position versus SMA**

   ```text
   position = (90 - 99.5) / 99.5 * 100
            = -9.547738693%
   ```

4. **5-day versus 20-day SMA trend**

   The last five prices are `[100, 100, 100, 100, 90]`:

   ```text
   sma5 = (100 + 100 + 100 + 100 + 90) / 5
        = 98
   trend = (98 - 99.5) / 99.5 * 100
         = -1.507537688%
   ```

5. **Normalised components**

   ```text
   momentum_component = clamp(50 + (-10) * 5, 0, 100)
                      = 0
   position_component = clamp(50 + (-9.547738693) * 5, 0, 100)
                      = 2.261306535
   trend_component = clamp(50 + (-1.507537688) * 5, 0, 100)
                   = 42.46231156
   ```

6. **Weighted total and label**

   ```text
   score = 0.40 * 0 + 0.40 * 2.261306535 + 0.20 * 42.46231156
         = 9.396984923
         = 9.4 after rounding
   label = Weak indicators
   ```

## Limitations

- This is a documented heuristic, not validated investment advice.
- The score is not a prediction and does not guarantee returns.
- Components saturate at 0 and 100 once the input percentage reaches -10% or +10% because of the scale of 5.
- The momentum base is the first price in the latest 20-price window (`prices[-20]`), as implemented. It is not necessarily the price from exactly 20 trading sessions if the input series includes gaps or non-trading dates.