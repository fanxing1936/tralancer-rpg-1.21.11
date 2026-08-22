execute as @s at @s store result score @s random run random value 1..4
execute as @s[scores={random=1}] at @s run tellraw @s ["",{"text":"“从今往后，","bold":true},{"text":"高悬的烈日将指引你前进，指引你不择手段的前进”","bold":true,"color":"red"}]
execute as @s[scores={random=2}] at @s run tellraw @s ["",{"text":"“从今往后，","bold":true},{"text":"无论深渊还是山巅，你将不惧死亡，直到一切的尽头”","bold":true,"color":"gold"}]
execute as @s[scores={random=3}] at @s run tellraw @s ["",{"text":"“从今往后，","bold":true},{"text":"风将化作你的眼睛，带你看尽世间的芳华”","bold":true,"color":"green"}]
execute as @s[scores={random=4}] at @s run tellraw @s ["",{"text":"“从今往后，","bold":true},{"text":"波涛的海水将审判罪恶之人”","bold":true,"color":"aqua"}]
