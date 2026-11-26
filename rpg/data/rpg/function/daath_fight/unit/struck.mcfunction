# 挨了一下：#d 是原始伤害（十分之一点）。每下最多按本段生命的 1.2% 算，再按明暗、夺甲折算
execute if entity @s[tag=rpg.dt.morph] run return 0
execute if entity @s[tag=rpg.dt.desp] run return 0
scoreboard players operation #cap rpg_dt = @s rpg_dt_mx
scoreboard players operation #cap rpg_dt *= #12 rpg_dt
scoreboard players operation #cap rpg_dt /= #100 rpg_dt
execute if score #d rpg_dt > #cap rpg_dt run scoreboard players operation #d rpg_dt = #cap rpg_dt
execute if entity @s[tag=rpg.dt.seek] run tag @s add rpg.dt.found
execute if entity @s[tag=rpg.dt.window] run function rpg:daath_fight/clash/win
execute if score @s rpg_dt_shell matches 1.. run return run function rpg:daath_fight/shell/hit
scoreboard players set #pc rpg_dt 100
execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 1 run scoreboard players set #pc rpg_dt 60
execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 2 run scoreboard players set #pc rpg_dt 75
execute if entity @s[tag=rpg.dt.lit] run scoreboard players set #pc rpg_dt 150
execute if score @s rpg_dt_sk matches 20 run scoreboard players set #pc rpg_dt 150
# 夺了盔甲：受到的伤害 −20%
execute if score @s rpg_dt_sa matches 1.. run scoreboard players operation #pc rpg_dt *= #8 rpg_dt
execute if score @s rpg_dt_sa matches 1.. run scoreboard players operation #pc rpg_dt /= #10 rpg_dt
# 同一招用太多：减半
execute if entity @s[tag=rpg.dt.loop] run scoreboard players set #k rpg_dt 2
execute if entity @s[tag=rpg.dt.loop] run scoreboard players operation #pc rpg_dt /= #k rpg_dt
execute if score @s rpg_dt_sk matches 3 if entity @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/guard/struck
scoreboard players operation #e rpg_dt = #d rpg_dt
scoreboard players operation #e rpg_dt *= #pc rpg_dt
scoreboard players operation #e rpg_dt /= #100 rpg_dt
scoreboard players operation @s rpg_dt_h -= #e rpg_dt
execute if score @s rpg_dt_h matches ..10 run scoreboard players set @s rpg_dt_h 10
# 计数：近战第几下、是不是一直同一格武器
execute if entity @a[tag=rpg.dt.me,distance=..5.5] run function rpg:daath_fight/mind/melee
execute if entity @s[tag=rpg.dt.lit] if score #d rpg_dt matches 10.. run function rpg:daath_fight/steal/pry
playsound minecraft:block.glass.hit hostile @a[distance=..24] ~ ~ ~ 0.5 0.8
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~1.1 ~ 0.25 0.4 0.25 0 4
execute if entity @s[tag=rpg.dt.drk] run function rpg:daath_fight/drink/hit
