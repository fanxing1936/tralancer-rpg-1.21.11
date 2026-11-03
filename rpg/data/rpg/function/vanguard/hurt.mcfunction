# 先锋罪仆挨了一下。
playsound rpg:vanguard.hurt hostile @a[distance=..24] ~ ~ ~ 1 1
execute if entity @s[tag=!rpg.vg.broken] run function rpg:vanguard/shield_break
