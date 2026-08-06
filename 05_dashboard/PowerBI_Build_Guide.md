# My Power BI Build Statement
### Mubadala Portfolio Strategy report

I built the data model and wrote the DAX; I shipped a
browser dashboard since I work on a Mac.

- *I modelled it as a star schema so one sector slicer filters holdings, deals and market
  data through a single dimension, rather than duplicating text across a flat table.*
- *I wrote a disclosure-rate measure because thirteen of nineteen deals have no published
  value. Reporting a 'total deal value' from public sources would have been misleading, so
  the report shows the disclosed floor and labels it as such.*
- *The concentration measure is a Herfindahl index in DAX; it comes out at 2,734, which
  is formally concentrated, and the effective number of independent buckets is 3.7 rather
  than 5.*
- *I built the browser version because I'm on a Mac. The data model and the DAX are in the
  repository.*
