scoreboard players set #state rpg_pr 0
scoreboard players set #cut rpg_pr 0
scoreboard players set #rift rpg_pr 0
scoreboard players set #aura rpg_pr 0
scoreboard players set #smoke rpg_pr 0
scoreboard players set #bgm rpg_pr 0
scoreboard players set #pro rpg_mk 0
execute if score #fight rpg_mk matches 1 run function rpg:michael_boss/clear
execute as @e[type=minecraft:vindicator,tag=rpg.pr.actor] run function rpg:prologue/cut/kill_actor
execute as @e[tag=rpg.pr.foe] run function rpg:prologue/cut/kill_actor
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] run function rpg:prologue/cut/kill_actor
kill @e[tag=rpg.pr.ent]
function rpg:prologue/sub/clear
bossbar set rpg:prologue_zh visible false
bossbar set rpg:prologue_en visible false
bossbar set rpg:prologue_zh players
bossbar set rpg:prologue_en players
execute in rpg:armageddon run forceload remove -64 -64 63 63
