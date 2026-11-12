# as 玩家 at 玩家：脚下一根，外加三角三根。
summon minecraft:marker ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu2f.vmark","rpg.lu2f.new"]}
summon minecraft:marker ~2.2 ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu2f.vmark","rpg.lu2f.new"]}
summon minecraft:marker ~-1.1 ~ ~1.9 {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu2f.vmark","rpg.lu2f.new"]}
summon minecraft:marker ~-1.1 ~ ~-1.9 {Tags:["rpg.lu2f.fx","rpg.lu2f.mark","rpg.lu2f.vmark","rpg.lu2f.new"]}
function rpg:lucifer_fight/vine/mark_fx
execute positioned ~2.2 ~ ~ run function rpg:lucifer_fight/vine/mark_fx
execute positioned ~-1.1 ~ ~1.9 run function rpg:lucifer_fight/vine/mark_fx
execute positioned ~-1.1 ~ ~-1.9 run function rpg:lucifer_fight/vine/mark_fx
