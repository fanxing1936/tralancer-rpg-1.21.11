clear @s minecraft:echo_shard[minecraft:custom_data~{rpg_sealed:1b,rpg_lord:5}] 1
scoreboard players add @s rpg_taint 15
execute at @s run function rpg:taint/lord5
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[封印逃逸] ","color":"#7B241C","bold":true,"italic":false},{"text":"萨麦尔的残魂从遗物中重新降临。","color":"gray","italic":false}]
playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..32] ~ ~ ~ 1 0.55
function rpg:inquest/seal/reindex
