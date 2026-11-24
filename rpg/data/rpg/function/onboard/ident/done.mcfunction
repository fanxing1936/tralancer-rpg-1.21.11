scoreboard players set @s rpg_ob 5
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.5 1.4
execute if score @s rpg_messiah matches 1 run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 0.8
function rpg:onboard/show
