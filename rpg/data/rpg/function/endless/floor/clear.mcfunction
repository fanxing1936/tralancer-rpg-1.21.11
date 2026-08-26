scoreboard players set @s rpg_end_state 2
scoreboard players set @s rpg_end_time 0
scoreboard players set @a[tag=rpg.end.member.current] rpg_end_claim 0
scoreboard players set @a[tag=rpg.end.member.current] rpg_end_pick 0
scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_pick
execute as @a[tag=rpg.end.member.current] if score @s rpg_end_best < #floor rpg_end_tmp run scoreboard players operation @s rpg_end_best = #floor rpg_end_tmp
execute as @a[tag=rpg.end.member.current] run function rpg:endless/reward/base_xp
bossbar set rpg:endless value 0
bossbar set rpg:endless color yellow
bossbar set rpg:endless name ["",{"text":"层结算｜第 ","color":"#D4AF37","bold":true,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" 层 · 选择一项恩赐","color":"#D4AF37","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @a[tag=rpg.end.member.current,distance=..96] ~ ~ ~ 0.75 1.15
execute as @a[tag=rpg.end.member.current] run function rpg:endless/reward/open
