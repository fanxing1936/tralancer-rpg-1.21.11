scoreboard players set #state rpg_pr_i1 0
scoreboard players set #cut rpg_pr_i1 0
scoreboard players set #rift rpg_pr_i1 0
scoreboard players set #aura rpg_pr_i1 0
scoreboard players set #smoke rpg_pr_i1 0
scoreboard players set #bgm rpg_pr_i1 0
scoreboard players set #pro rpg_mk_i1 0
execute if score #fight rpg_mk_i1 matches 1 run function rpg:michael_boss_i1/clear
execute as @e[type=minecraft:vindicator,tag=rpg.pr.actor,distance=0..] run function rpg:prologue_i1/cut/kill_actor
execute as @e[tag=rpg.pr.foe,distance=0..] run function rpg:prologue_i1/cut/kill_actor
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] run function rpg:prologue_i1/cut/kill_actor
kill @e[tag=rpg.pr.ent,distance=0..]
function rpg:prologue_i1/sub/clear
bossbar set rpg:prologue_zh_i1 visible false
bossbar set rpg:prologue_en_i1 visible false
bossbar set rpg:prologue_zh_i1 players
bossbar set rpg:prologue_en_i1 players
execute in rpg:armageddon run forceload remove -64 -64 63 63
