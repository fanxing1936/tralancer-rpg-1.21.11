$execute store result score #len rpg_dt run data get storage rpg:daath s$(n).arms
execute if score #len rpg_dt matches 18.. run return 0
$data modify storage rpg:daath s$(n).arms append from storage rpg:daath t.e
