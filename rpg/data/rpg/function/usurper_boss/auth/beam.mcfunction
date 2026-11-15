scoreboard players set #d rpg_ub 0
function rpg:usurper_boss/infuse/step
execute as @e[tag=rpg.usb.abeam] if score @s rpg_ub_id = #id rpg_ub run function rpg:usurper_boss/auth/set
