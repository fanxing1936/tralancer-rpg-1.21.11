data modify storage rpg:town m.sfx set value ""
$execute positioned ~40 $(y) ~-11 run function rpg:town/b/orc_camp/180 with storage rpg:town m
$execute positioned ~24 $(y) ~-24 run summon minecraft:marker ~ ~2 ~ {Tags:["rpg.tw.a","rpg.tw.at.camp","rpg.tw.new"]}
