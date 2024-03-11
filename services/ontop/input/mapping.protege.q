[QueryItem="get-victims"]
PREFIX : <http://example.org/pinochet-rettig#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?victim ?lastName {
  ?victim a :Victim ; foaf:lastName ?lastName .
}