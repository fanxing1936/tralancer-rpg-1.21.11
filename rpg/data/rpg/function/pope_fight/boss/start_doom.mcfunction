scoreboard players set #sk rpg_pf 13
scoreboard players set #st rpg_pf 0
function rpg:pope_fight/clip/summon
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔓𝔬𝔭𝔢","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"最后的审判：","color":"#E6DFCF","bold":false,"italic":false},{"text":"圣所之外，皆是罪土。","color":"#9C9A94","bold":false,"italic":false}]
playsound rpg:pope.load_spell hostile @a[distance=..64] ~ ~ ~ 1 0.6
particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 normal
