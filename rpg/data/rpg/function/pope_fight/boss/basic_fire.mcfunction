# 普攻：一发快弹。
execute positioned ^-0.05 ^0.09 ^2.22 facing entity @a[distance=..32,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] eyes run function rpg:pope_fight/fx/blast_quick
playsound rpg:pope.spell hostile @a[distance=..32] ~ ~ ~ 0.5 1.4
