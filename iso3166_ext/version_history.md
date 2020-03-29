

#### ver. 0.0.2

Decided to abandon the use of .csv (comma separated values) 
since several official country names use ',' in the form 
"Saint Helena, Ascension and Tristan da Cunha" or 
"Tanzania, the United Republic of" and that is just a load 
of troubles...

Shifting to .tab (Tabulator separated values) and expect 
that to provide a world of relief...


#### ver. 0.0.1

Early mess around. 

Wanted to create an Extendable iso 3166 module, which 
allowed for Easy User-extension of the data collection.

Original use case was a need for an iso 3166 module, that 
also allowed search by international ship codes, 
i.e. MID as in AIS system.

The goal is an iso 3166-1 complete (249 territories) data
 collection, that include all (5?) default keys; alpha-2, 
 alpha-3, numeric-3, name_en, official_name_en.
And is easily extendable with as many new keys as I like.

The idae is that each new key is stored in a .csv file holding
two columns. The first column is an existing key, preferable
alpha-2, and the other column is the values of the new key, 
e.g. MID.
