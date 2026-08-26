tellraw @a[tag=rpg.end.member.current,distance=..96] ["",{"text":"[回廊闭合] ","color":"#FF665E","bold":true,"italic":false},{"text":"本次挑战已结束，历史最深层记录保留。","color":"#AAB4C3","bold":false,"italic":false}]
tp @e[tag=rpg.end.enemy] ~ -200 ~
kill @e[tag=rpg.end.enemy]
execute as @a[tag=rpg.end.member.current] run function rpg:endless/member/stale_cleanup
bossbar set rpg:endless players
bossbar set rpg:endless value 0
kill @s
