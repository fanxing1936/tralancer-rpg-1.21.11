data modify storage rpg:town m.sfx set value ""
$execute positioned ~-11 $(y) ~-16 run function rpg:town/b/orc_camp/cw with storage rpg:town m
$execute positioned ~-24 $(y) ~0 run summon minecraft:marker ~ ~2 ~ {Tags:["rpg.tw.a","rpg.tw.at.camp","rpg.tw.new"]}
