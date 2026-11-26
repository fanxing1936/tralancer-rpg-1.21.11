scoreboard players set @s rpg_dt_sk 3
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/guard
scoreboard players set @s rpg_dt_mel 0
scoreboard players set @s rpg_dt_gcd 160
function rpg:daath_fight/eye/blade
playsound minecraft:item.armor.equip_chain hostile @a[distance=..48] ~ ~ ~ 1 0.8
