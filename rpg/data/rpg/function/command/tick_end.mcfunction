# Commit this tick's health snapshot; runs last in #minecraft:tick.
execute as @e[tag=rpg.hurt] run scoreboard players operation @s damage_timing = @s damage_action
