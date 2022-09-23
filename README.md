# PromQL tester

Promql tester is a tool that can be used to test promql expressions.
It can be useful to validate health of deployments.

The application reads conditions from a given file
specified in `CONDITIONS_PATH` env var, and runs promql expresions
against a given prometheus url specified in env var `PROMETHEUS_URL`.

### Conditions

Conditions describe what should be tested, how often and for how long.
Conditions need to be specified in a yaml config file.


#### Example

```yaml
conditions:
- expression: 'sum(increase(elasticsearch_indices_shards_docs{primary="true",index=~"foobar.*"}[5m])) - sum(increase(elasticsearch_indices_shards_docs{primary="true",index=~"foobar.*"}[5m] offset 5m))'
  for_seconds: 300
  interval_seconds: 30
  threshold:
    upper: 10
    lower: -10
```

The above condition will check that the 5m increase of the documents is the same as the increase with offset 5m.
This condition will be evaluated for 300 seconds each 30 seconds.
If the condition stays within the specified threshold for the whole duration, the condition is successful.
However if the condition falls outside the specified threshold, it will fail.
