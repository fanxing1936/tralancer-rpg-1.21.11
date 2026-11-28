scoreboard players set #state rpg_pr_i2 0
scoreboard players set #cut rpg_pr_i2 0
scoreboard players set #rift rpg_pr_i2 0
scoreboard players set #aura rpg_pr_i2 0
scoreboard players set #smoke rpg_pr_i2 0
scoreboard players set #bgm rpg_pr_i2 0
scoreboard players set #pro rpg_mk_i2 0
execute if score #fight rpg_mk_i2 matches 1 run function rpg:michael_boss_i2/clear
execute as @e[type=minecraft:vindicator,tag=rpg.pr.actor,distance=0..] run function rpg:prologue_i2/cut/kill_actor
execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i2/cut/kill_actor
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] run function rpg:prologue_i2/cut/kill_actor
kill @e[tag=rpg.pr.ent,distance=0..]
function rpg:prologue_i2/sub/clear
bossbar set rpg:prologue_zh_i2 visible false
bossbar set rpg:prologue_en_i2 visible false
bossbar set rpg:prologue_zh_i2 players
bossbar set rpg:prologue_en_i2 players
execute in rpg:armageddon_2 run forceload remove -64 -64 63 63
