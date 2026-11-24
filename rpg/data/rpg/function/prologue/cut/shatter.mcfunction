# 米迦勒一脚踩碎石台：石台方块拆掉，碎块往下掉
execute in rpg:armageddon run fill -4 80 -4 4 80 4 minecraft:air replace #rpg:prologue_platform
execute in rpg:armageddon run particle minecraft:block{block_state:"minecraft:polished_blackstone_bricks"} 0 80.5 0 2.5 0.4 2.5 0.2 300 force
execute in rpg:armageddon run particle minecraft:explosion 0 80.5 0 2 0.3 2 0 6 force
kill @e[type=minecraft:item_display,tag=rpg.pr.spine]
execute in rpg:armageddon run summon minecraft:marker 0 36.5 0 {Tags:["rpg.pr.smoke","rpg.pr.ent"]}
