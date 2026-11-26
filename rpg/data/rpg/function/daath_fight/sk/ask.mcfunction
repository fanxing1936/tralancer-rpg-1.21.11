scoreboard players operation #m rpg_dt = @s rpg_dt_t
scoreboard players set #k rpg_dt 20
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute if score @s rpg_dt_t matches 10..110 if score #m rpg_dt matches 0 run playsound minecraft:block.note_block.hat hostile @a[distance=..48] ~ ~ ~ 0.8 0.8
execute if score @s rpg_dt_t matches 122 run function rpg:daath_fight/ask/judge
execute if score @s rpg_dt_t matches 176.. run function rpg:daath_fight/sk/end
