tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……圣血祭被打断了。","color":"#9C9A94","bold":false,"italic":false}]
kill @e[tag=rpg.pf.line]
playsound rpg:pope.spell_disappear hostile @a[distance=..32] ~ ~ ~ 1 1
function rpg:pope_fight/boss/end
