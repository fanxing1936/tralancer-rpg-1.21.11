scoreboard players operation #h rpg_dt = @s rpg_dt_mx
scoreboard players set #k rpg_dt 2
scoreboard players operation #h rpg_dt *= #k rpg_dt
scoreboard players operation @s rpg_dt_h = #h rpg_dt
function rpg:daath_fight/bar/set
