from typing import NamedTuple

from falmer.grooves.grooves import GroovesQuery


class EventSparklineVariables(NamedTuple):
    event_id: int
    interval: str
    length: str


event_sparkline = GroovesQuery[EventSparklineVariables](
    'eventanalytics',
    """
      select (
        select count(*)
        from event
        where name = 'Event Viewed'
        and properties ->> 'eventId' = $1
        and time between (series.endtime - $2::interval) and series.endtime
      ) as hits,
      series.endtime as time
      from (
        select generate_series(date_trunc('hour', now()) - $3::interval, date_trunc('hour', now()), $2) as endtime
      ) series
    """,
    cache=600,
    postprocess=lambda result: [row['hits'] for row in result]
)
