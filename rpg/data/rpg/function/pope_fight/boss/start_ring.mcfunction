scoreboard players set #sk rpg_pf 9
scoreboard players set #st rpg_pf 0
function rpg:pope_fight/clip/cast
execute positioned ^0.43 ^2.90 ^0.57 run function rpg:pope_fight/fx/charge
playsound rpg:pope.load_spell hostile @a[distance=..32] ~ ~ ~ 0.7 1
