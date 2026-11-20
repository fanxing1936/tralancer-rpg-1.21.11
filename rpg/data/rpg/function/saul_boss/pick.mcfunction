scoreboard players set @s rpg_sl_n 0
scoreboard players set #ult rpg_sl 0
# 二阶段血量到 150：只放一次的疯王之舞
execute if score @s rpg_sl matches 2 if score @s rpg_sl_h matches ..150 unless entity @s[tag=rpg.slb.danced] run return run function rpg:saul_boss/ult/dance
execute if score @s rpg_sl matches 1 if score @s rpg_sl_h matches ..750 unless entity @s[tag=rpg.slb.u1] run scoreboard players set #ult rpg_sl 1
execute if score @s rpg_sl matches 1 if score @s rpg_sl_h matches ..500 unless entity @s[tag=rpg.slb.u2] run scoreboard players set #ult rpg_sl 2
execute if score @s rpg_sl matches 1 if score @s rpg_sl_h matches ..250 unless entity @s[tag=rpg.slb.u3] run scoreboard players set #ult rpg_sl 3
execute if score @s rpg_sl matches 1 if score #ult rpg_sl matches 0 if score @s rpg_sl_c matches 900.. run scoreboard players set #ult rpg_sl 9
execute if score @s rpg_sl matches 2 if score @s rpg_sl_h matches ..750 unless entity @s[tag=rpg.slb.u1] run scoreboard players set #ult rpg_sl 1
execute if score @s rpg_sl matches 2 if score @s rpg_sl_h matches ..500 unless entity @s[tag=rpg.slb.u2] run scoreboard players set #ult rpg_sl 2
execute if score @s rpg_sl matches 2 if score @s rpg_sl_h matches ..250 unless entity @s[tag=rpg.slb.u3] run scoreboard players set #ult rpg_sl 3
execute if score @s rpg_sl matches 2 if score #ult rpg_sl matches 0 if score @s rpg_sl_c matches 1100.. run scoreboard players set #ult rpg_sl 9
execute if score #ult rpg_sl matches 1.. run return run function rpg:saul_boss/ult/pick
# 被拉开到 6 格外：优先突刺
execute if score @s rpg_sl matches 1 unless entity @e[tag=rpg.unit.f,distance=..6] run return run function rpg:saul_boss/skill/lunge
execute if score @s rpg_sl matches 2 unless entity @e[tag=rpg.unit.f,distance=..6] run return run function rpg:saul_boss/skill/lunge3
execute if score @s rpg_sl matches 1 run scoreboard players operation #r rpg_sl = @s rpg_sl_k
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 0 run function rpg:saul_boss/skill/lunge
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 1 run function rpg:saul_boss/skill/guard
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 2 run function rpg:saul_boss/skill/flash
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 3 run function rpg:saul_boss/skill/shadow
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 4 run function rpg:saul_boss/skill/echo
execute if score @s rpg_sl matches 1 if score #r rpg_sl matches 5 run function rpg:saul_boss/skill/lunge
execute if score @s rpg_sl matches 1 run scoreboard players add @s rpg_sl_k 1
execute if score @s rpg_sl matches 1 if score @s rpg_sl_k matches 6.. run scoreboard players set @s rpg_sl_k 0
execute if score @s rpg_sl matches 2 run scoreboard players operation #r rpg_sl = @s rpg_sl_k
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 0 run function rpg:saul_boss/skill/lunge3
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 1 run function rpg:saul_boss/skill/thrusts
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 2 run function rpg:saul_boss/skill/web
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 3 run function rpg:saul_boss/skill/step
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 4 run function rpg:saul_boss/skill/guard
execute if score @s rpg_sl matches 2 if score #r rpg_sl matches 5 run function rpg:saul_boss/skill/feint
execute if score @s rpg_sl matches 2 run scoreboard players add @s rpg_sl_k 1
execute if score @s rpg_sl matches 2 if score @s rpg_sl_k matches 6.. run scoreboard players set @s rpg_sl_k 0
