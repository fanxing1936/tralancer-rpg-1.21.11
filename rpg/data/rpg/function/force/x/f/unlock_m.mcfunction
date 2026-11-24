scoreboard players set @s rpg_k26 1
function rpg:force/page/fill
function rpg:force/x/f/auto_m
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"王冠阶 · 习得终式 ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"p.n26","storage":"rpg:force","color":"#A276BE","bold":true},{"text":"。在技能页「王冠 · 传承」里放进槽。","color":"#E6DFCF","bold":false,"italic":false}]
