clear

cd "/home/joseph/aa-data/raw"

insheet using MasterCSV_GROUP2.csv, comma names

//  Drops students from the pilot data (39 observations)
drop if externaldatareference == "Anna" || externaldatareference == "Lily" || ///
	externaldatareference == "Taft"
	
save group1, replace

clear

insheet using MasterCSV_GROUP3_2.csv, comma names

save group2, replace
	
	
