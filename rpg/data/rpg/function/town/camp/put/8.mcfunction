data modify storage rpg:town m.sfx set value ""
$execute positioned ~8 $(y) ~10 run function rpg:town/b/orc_camp/none with storage rpg:town m
$execute positioned ~24 $(y) ~24 run summon minecraft:marker ~ ~2 ~ {Tags:["rpg.tw.a","rpg.tw.at.camp","rpg.tw.new"]}
