# 击败结算：清魔化，收束。
scoreboard players set @a[distance=..48] rpg_taint 0
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔓𝔬𝔭𝔢","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"「你们必晓得真理，真理必叫你们得以自由。」——《约翰福音》8:32","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @a[distance=..48] ~ ~ ~ 1 1
function rpg:pope_fight/clear
