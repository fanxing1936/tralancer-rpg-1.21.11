tag @s add rpg.rite.anchor.active
scoreboard players add @a[tag=rpg.rite.chooser,distance=..10] rpg_ex_xp 20
tellraw @a[distance=..20,gamemode=!spectator] ["",{"text":"〖裁决・放逐〗","color":"#CDBE86","bold":true,"italic":false},{"text":" 𝔅𝔞𝔫𝔦𝔰𝔥","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"完整判词将恶魔逐离此世。","color":"#9C9A94","italic":false}]
function rpg:inquest/anchor_success
