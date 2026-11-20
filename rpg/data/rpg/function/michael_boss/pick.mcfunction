scoreboard players set @s rpg_mk_n 0
scoreboard players set #ult rpg_mk 0
# 二阶段血量到 150：只放一次的六翼燃尽
execute if score @s rpg_mk matches 2 if score @s rpg_mk_h matches ..150 unless entity @s[tag=rpg.mkb.burnt] run return run function rpg:michael_boss/ult/burn
execute if score @s rpg_mk matches 1 if score @s rpg_mk_h matches ..900 unless entity @s[tag=rpg.mkb.u1] run scoreboard players set #ult rpg_mk 1
execute if score @s rpg_mk matches 1 if score @s rpg_mk_h matches ..600 unless entity @s[tag=rpg.mkb.u2] run scoreboard players set #ult rpg_mk 2
execute if score @s rpg_mk matches 1 if score @s rpg_mk_h matches ..300 unless entity @s[tag=rpg.mkb.u3] run scoreboard players set #ult rpg_mk 3
execute if score @s rpg_mk matches 1 if score #ult rpg_mk matches 0 if score @s rpg_mk_c matches 900.. run scoreboard players set #ult rpg_mk 9
execute if score @s rpg_mk matches 2 if score @s rpg_mk_h matches ..900 unless entity @s[tag=rpg.mkb.u1] run scoreboard players set #ult rpg_mk 1
execute if score @s rpg_mk matches 2 if score @s rpg_mk_h matches ..600 unless entity @s[tag=rpg.mkb.u2] run scoreboard players set #ult rpg_mk 2
execute if score @s rpg_mk matches 2 if score @s rpg_mk_h matches ..300 unless entity @s[tag=rpg.mkb.u3] run scoreboard players set #ult rpg_mk 3
execute if score @s rpg_mk matches 2 if score #ult rpg_mk matches 0 if score @s rpg_mk_c matches 1100.. run scoreboard players set #ult rpg_mk 9
execute if score #ult rpg_mk matches 1.. run return run function rpg:michael_boss/ult/pick
# 被拉开到 8 格外：一阶段天降，二阶段炽翼突进
execute if score @s rpg_mk matches 1 unless entity @e[tag=rpg.unit.f,distance=..8] run return run function rpg:michael_boss/skill/dive
execute if score @s rpg_mk matches 2 unless entity @e[tag=rpg.unit.f,distance=..8] run return run function rpg:michael_boss/skill/dash
execute if score @s rpg_mk matches 1 run scoreboard players operation #r rpg_mk = @s rpg_mk_k
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 0 run function rpg:michael_boss/skill/watch
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 1 run function rpg:michael_boss/skill/quis
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 2 run function rpg:michael_boss/skill/feather
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 3 run function rpg:michael_boss/skill/gaze
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 4 run function rpg:michael_boss/skill/dive
execute if score @s rpg_mk matches 1 if score #r rpg_mk matches 5 run function rpg:michael_boss/skill/fold
execute if score @s rpg_mk matches 1 run scoreboard players add @s rpg_mk_k 1
execute if score @s rpg_mk matches 1 if score @s rpg_mk_k matches 6.. run scoreboard players set @s rpg_mk_k 0
execute if score @s rpg_mk matches 2 run scoreboard players operation #r rpg_mk = @s rpg_mk_k
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 0 run function rpg:michael_boss/skill/watch
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 1 run function rpg:michael_boss/skill/dash
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 2 run function rpg:michael_boss/skill/cross
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 3 run function rpg:michael_boss/skill/gaze
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 4 run function rpg:michael_boss/skill/rain
execute if score @s rpg_mk matches 2 if score #r rpg_mk matches 5 run function rpg:michael_boss/skill/dash
execute if score @s rpg_mk matches 2 run scoreboard players add @s rpg_mk_k 1
execute if score @s rpg_mk matches 2 if score @s rpg_mk_k matches 6.. run scoreboard players set @s rpg_mk_k 0
