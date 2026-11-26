# 空着手：走近，等间隔，选下一招（as/at 影子）
function rpg:daath_fight/eye/follow
scoreboard players remove @s rpg_dt_gap 1
# 贴得太近就停住、退半步
execute if entity @a[tag=rpg.dt.me,distance=..1.5] run function rpg:daath_fight/unit/room
execute if score @s rpg_dt_gap matches 1.. if entity @a[tag=rpg.dt.me,distance=..1.9] run return run data merge entity @s {NoAI:1b}
execute if score @s rpg_dt_gap matches 1.. run return run data merge entity @s {NoAI:0b}
execute if score @s rpg_dt_st matches 1 run scoreboard players set @s rpg_dt_gap 16
execute if score @s rpg_dt_st matches 2 run scoreboard players set @s rpg_dt_gap 10
function rpg:daath_fight/pick
