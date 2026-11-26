# 选招：大招血线 → 影版技能 → 它记住的事 → 夺械 → 连招
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_st matches 1 if score @s rpg_dt_bar matches ..13 unless entity @s[tag=rpg.dt.u1] run return run function rpg:daath_fight/ult/1_1
execute if score @s rpg_dt_st matches 1 if score @s rpg_dt_bar matches ..7 unless entity @s[tag=rpg.dt.u2] run return run function rpg:daath_fight/ult/1_2
execute if score @s rpg_dt_st matches 2 if score @s rpg_dt_bar matches ..14 unless entity @s[tag=rpg.dt.u1] run return run function rpg:daath_fight/ult/2_1
execute if score @s rpg_dt_st matches 2 if score @s rpg_dt_bar matches ..8 unless entity @s[tag=rpg.dt.u2] run return run function rpg:daath_fight/ult/2_2
execute if score @s rpg_dt_st matches 2 if score @s rpg_dt_bar matches ..4 unless entity @s[tag=rpg.dt.u3] run return run function rpg:daath_fight/ult/2_3
execute if score @s rpg_dt_ek matches 1.. if score @s rpg_dt_et matches 0 run return run function rpg:daath_fight/echo/cast
execute if entity @s[tag=rpg.dt.want_drink] run return run function rpg:daath_fight/skill/drink
execute if score @s rpg_dt_far matches 80.. run return run function rpg:daath_fight/skill/step
execute if score @s rpg_dt_still matches 60.. if entity @a[tag=rpg.dt.me,distance=..9] run return run function rpg:daath_fight/skill/grab
execute if score @s rpg_dt_mel matches 5.. if score @s rpg_dt_gcd matches 0 run return run function rpg:daath_fight/skill/guard
execute if score @s rpg_dt_scd matches 0 if entity @a[tag=rpg.dt.me,distance=..9] run return run function rpg:daath_fight/skill/steal
execute store result score #r rpg_dt run random value 1..100
execute if score @s rpg_dt_st matches 1 if score #r rpg_dt matches 1..14 run return run function rpg:daath_fight/skill/dodge
execute if score @s rpg_dt_st matches 2 if score #r rpg_dt matches 1..12 run return run function rpg:daath_fight/skill/follow
execute if score @s rpg_dt_st matches 2 if score #r rpg_dt matches 13..24 if entity @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..40] run return run function rpg:daath_fight/skill/douse
execute if score @s rpg_dt_st matches 2 if score #r rpg_dt matches 25..36 run return run function rpg:daath_fight/skill/swap
execute if score @s rpg_dt_st matches 2 if score #r rpg_dt matches 37..48 run return run function rpg:daath_fight/skill/pact
function rpg:daath_fight/skill/chain
