"""Jungle Abomination sounds: source-notify timing, lossless Wiki Ogg registry.

No file writes at import. This module owns neither gameplay nor phase switching.
Use configuration(ref) for Mob arguments, validate_sources(ref) for provenance,
and write_debug_functions(dp) for explicit sound audition (including music).
Fixed cooked volumes are preserved. Undetermined/default/random pitch remains 1
and is reported; this is not a recreation of Unreal attenuation/concurrency.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re


_PREFIX = 'DLC_Mob_Abom_'
_GROUPS = {
    'attack_boom': ('重击轰鸣（原用途未证实）', 'Attack boom (use unverified)', ['Attack_BOOM_Foley']),
    'basic_attack_foley': ('挥动躯干', 'Body attacks', ['BasicAttack_Foley']),
    'basic_attack_voice': ('攻击低吼', 'Attack vocal', ['BasicAttack_Vocal','BasicAttack2_Vocal']),
    'death_foley': ('躯体倒下', 'Body dies', ['Death_Foley']),
    'death_voice': ('死亡低吼', 'Death vocal', ['Death_Vocal']),
    'fall_foley': ('躯体失衡', 'Body falls', ['Fall_Foley']),
    'fall_voice': ('失衡低吼', 'Fall vocal', ['Fall_Vocal']),
    'flower_loop': ('花朵持续作响', 'Flower loop', ['Flower_LOOP']),
    'flower_close': ('花朵闭合', 'Flower closes', ['FlowerClose']),
    'flower_open': ('花朵展开', 'Flower opens', ['FlowerOpen']),
    'hurt_foley': ('躯体受击', 'Body hurt', ['GetHit1_Foley','GetHit2_Foley','GetHit3_Foley']),
    'hurt_voice': ('受伤低吼', 'Hurt vocal', ['GetHit1_Vocal','GetHit2_Vocal','GetHit3_Vocal','GetHit4_Vocal']),
    'getup_foley': ('躯体起身', 'Body gets up', ['GetUp_Foley']),
    'getup_voice': ('起身低吼', 'Get-up vocal', ['GetUp_Vocal']),
    'idle_foley': ('枝干摩擦', 'Idle body', ['Idle_Foley']),
    'idle_voice': ('闲置低吼', 'Idle vocal', ['Idle_Vocal']),
    'intro_foley': ('登场躯体声', 'Intro body', ['Intro_Foley_STEREO']),
    'intro_voice': ('登场低吼', 'Intro vocal', ['Intro_Vocal_STEREO']),
    'land_foley': ('躯体落地', 'Body lands', ['Land_Foley']),
    'land_voice': ('落地低吼', 'Land vocal', ['Land_Vocal']),
    'laugh_voice': ('低沉笑声', 'Laugh', ['Laugh_Vocal_STEREO']),
    'summon_foley': ('召唤动作', 'Summon movement', ['Summon_Foley']),
    'summon_voice': ('召唤低吼', 'Summon vocal', ['Summon_Vocal']),
    'vine_attack_foley': ('藤蔓攻击动作', 'Vine attack movement', ['VineAttack_Foley']),
    'vine_attack_voice': ('藤蔓攻击低吼', 'Vine attack vocal', ['VineAttack_Vocal']),
    'vine_fail_foley': ('藤蔓失败动作', 'Vine failure movement', ['VineAttackFail_Foley']),
    'vine_fail_voice': ('藤蔓失败低吼', 'Vine failure vocal', ['VineAttackFail_Vocal']),
    'vine_success_foley': ('藤蔓命中动作', 'Vine success movement', ['VineAttackSuccess_Foley']),
    'vine_success_voice': ('藤蔓命中低吼', 'Vine success vocal', ['VineAttackSuccess_Vocal']),
    'walk_foley': ('沉重脚步', 'Heavy footsteps', ['Walk1_Foley','Walk2_Foley']),
    'walk_voice': ('行走低吼', 'Walking vocal', ['Walk1_Vocal','Walk2_Vocal']),
    'walk_legacy_foley': ('行走声音（未被当前通知引用）', 'Legacy walk Foley', ['Walk_Foley']),
    'walk_legacy_voice': ('行走低吼（未被当前通知引用）', 'Legacy walk vocal', ['Walk_Vocal']),
}
SOUNDS = {event: ((zh,en), [_PREFIX+f+'.ogg' for f in files], {})
          for event,(zh,en,files) in _GROUPS.items()}
for _suffix in ('Start','Loop','End'):
    SOUNDS['music_'+_suffix.lower()+'_preview'] = (
        ('首领音乐预览（'+_suffix+'）','Boss music preview ('+_suffix+')'),
        ['Bgm_env_sosw2DBossCauldron'+_suffix+'-001_soundWave.ogg'], {'stream':True})
SOUNDS['vine_burst_old'] = (('召唤藤蔓爆发（旧版）','Vine burst (old)'),['DLC_mob_abomvine_burst_F.ogg'],{})
SOUNDS['vine_burst_new'] = (('召唤藤蔓爆发（新版）','Vine burst (new)'),['DLC_mob_abomvine_burst_F_New.ogg'],{})
MUSIC_EVENTS = tuple(e for e in SOUNDS if e.startswith('music_'))

# Exact AnimNotify_DungeonsPlaySound references, not guessed clip/name matches.
_ASSET_EVENTS = {
    'DLC_Mob_Abom_BasicAtt':'basic_attack_foley', 'DLC_Mob_Abom_V_BasicAtt':'basic_attack_voice',
    'DLC_Mob_Abom_Death':'death_foley', 'DLC_Mob_Abom_V_Death':'death_voice',
    'DLC_Mob_Abom_Idle':'idle_foley', 'DLC_Mob_Abom_V_Idle':'idle_voice',
    'DLC_Mob_Abom_Land':'land_foley', 'DLC_Mob_Abom_V_Land':'land_voice',
    'DLC_Mob_Abom_Sum':'summon_foley', 'DLC_Mob_Abom_V_Sum':'summon_voice',
    'DLC_Mob_Abom_VineAtt':'vine_attack_foley', 'DLC_Mob_Abom_V_VineAtt':'vine_attack_voice',
    'DLC_Mob_Abom_VineAttSucc':'vine_success_foley', 'DLC_Mob_Abom_V_VineAttSucc':'vine_success_voice',
    'DLC_Mob_Abom_V_VineAttFail':'vine_fail_voice',
    'DLC_Mob_Abom_VunFall':'fall_foley', 'DLC_Mob_Abom_V_VunFall':'fall_voice',
    'DLC_Mob_Abom_FlowerOpen':'flower_open', 'DLC_Mob_Abom_FlowerClose':'flower_close',
    'DLC_Mob_Abom_Vun_GetUp':'getup_foley', 'DLC_Mob_Abom_V_Vun_Getup':'getup_voice',
    'DLC_Mob_Abom_Walk':'walk_foley', 'DLC_Mob_Abom_V_Walk':'walk_voice',
    'DLC_Mob_Abom_GetHit':'hurt_foley', 'DLC_Mob_Abom_V_GetHit':'hurt_voice',
    'DLC_Mob_Abom_Laugh':'laugh_voice', 'DLC_Mob_Abom_VineAttFail':'vine_fail_foley',
}
_ASSET_EVENTS = {name.lower(): event for name,event in _ASSET_EVENTS.items()}

# Captured UObject evidence is embedded so reproducibility does not require the
# export workstation's phase2_full directory. Source paths remain game paths.
SOURCE_NOTIFIES = [{'clip': 'jungleAbomination_Attack',
  'source_animation_sha256': '6faa53dbfb9b6f0a69894ce23d9d5d0d8a0a4cde8c9c5a818d73f0767ad6b84b',
  'time': 0.08685424,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_Attack:AnimNotify_DungeonsPlaySound_4'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_Attack.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_4',
                    'Outer': 'jungleAbomination_Attack',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_BasicAtt.DLC_Mob_Abom_BasicAtt',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'ae4827747f6fe49421a7604f3e944933c2d7adca2967563040f345856ad0d273'},
 {'clip': 'jungleAbomination_Attack',
  'source_animation_sha256': '6faa53dbfb9b6f0a69894ce23d9d5d0d8a0a4cde8c9c5a818d73f0767ad6b84b',
  'time': 1.1991489,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_Attack:AnimNotify_DungeonsPlaySound_6'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_Attack.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_6',
                    'Outer': 'jungleAbomination_Attack',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_BasicAtt.DLC_Mob_Abom_V_BasicAtt',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'bf76df94f7b854b88e226266f4d8aa51ec7cbe6e0e104b2014d8d553b9470888'},
 {'clip': 'jungleAbomination_Attack',
  'source_animation_sha256': '6faa53dbfb9b6f0a69894ce23d9d5d0d8a0a4cde8c9c5a818d73f0767ad6b84b',
  'time': 1.5364347,
  'offset': 0.0,
  'notify_name': 'PlayParticleEffect',
  'notify': {'ObjectName': "AnimNotify_PlayParticleEffect'jungleAbomination_Attack:AnimNotify_PlayParticleEffect_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_Attack.2'},
  'notify_object': {'Type': 'AnimNotify_PlayParticleEffect',
                    'Name': 'AnimNotify_PlayParticleEffect_0',
                    'Outer': 'jungleAbomination_Attack',
                    'Class': "UScriptClass'AnimNotify_PlayParticleEffect'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'PSTemplate': {'ObjectName': "ParticleSystem'PS_JungleAbominationShockwave'",
                                                  'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/PS_JungleAbominationShockwave.117'},
                                   'LocationOffset': {'X': 0.0, 'Y': 685.1231, 'Z': 0.0}}},
  'notify_object_sha256': '9021417c8d3be04eeeeaf05c08e2c1b4a2cc070c64e3ac0824ae87fd0fecbd9d'},
 {'clip': 'jungleAbomination_death',
  'source_animation_sha256': 'fea71e4070d46afbc908dabe24ceeaad3100914899461f32cc59fab00b9e56b6',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_death:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_death.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_death',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Death.DLC_Mob_Abom_Death',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'f09aeee6aa7c1b3f4d03236a62240b4e33f69c32df7fb310d5c19e99b61f2e10'},
 {'clip': 'jungleAbomination_death',
  'source_animation_sha256': 'fea71e4070d46afbc908dabe24ceeaad3100914899461f32cc59fab00b9e56b6',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_death:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_death.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_death',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Death.DLC_Mob_Abom_V_Death',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '35149382a8e39f7413c3f997702cf790114b0a8c834df0ac1be2e269246c673c'},
 {'clip': 'jungleAbomination_idle',
  'source_animation_sha256': '26c351b989c56b57ac7b02a72031f4b8a1cdad9b5b670ca3a6001a2717647674',
  'time': 0.058183,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_idle:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_idle.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_idle',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Idle.DLC_Mob_Abom_Idle',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '5a83e4b472008580d9d17bb126748491afb170be352d623dae351577dc813844'},
 {'clip': 'jungleAbomination_idle',
  'source_animation_sha256': '26c351b989c56b57ac7b02a72031f4b8a1cdad9b5b670ca3a6001a2717647674',
  'time': 1.7288662,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_idle:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_idle.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_idle',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Idle.DLC_Mob_Abom_V_Idle',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'ae698260aa48cf3358ac24c61df9769518b35c9c517a9f00066c3372c96be2b2'},
 {'clip': 'jungleAbomination_land',
  'source_animation_sha256': '9962ac81b45ef54f4ff850ad3b8345dc703d16211975b9d607cc970a80e48b46',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_land:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_land.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_land',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Land.DLC_Mob_Abom_Land',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '637c90017bb1059817f89f91891d3aced80eadeecc14db3cdc391602473d7d1a'},
 {'clip': 'jungleAbomination_land',
  'source_animation_sha256': '9962ac81b45ef54f4ff850ad3b8345dc703d16211975b9d607cc970a80e48b46',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_land:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_land.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_land',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Land.DLC_Mob_Abom_V_Land',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'c09016ad56ca85fbfef32ce8b161cc582befdcb7e7757b71f9cd353435e6a4a4'},
 {'clip': 'jungleAbomination_land',
  'source_animation_sha256': '9962ac81b45ef54f4ff850ad3b8345dc703d16211975b9d607cc970a80e48b46',
  'time': 0.037677303,
  'offset': 0.0,
  'notify_name': 'PlayParticleEffect',
  'notify': {'ObjectName': "AnimNotify_PlayParticleEffect'jungleAbomination_land:AnimNotify_PlayParticleEffect_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_land.2'},
  'notify_object': {'Type': 'AnimNotify_PlayParticleEffect',
                    'Name': 'AnimNotify_PlayParticleEffect_0',
                    'Outer': 'jungleAbomination_land',
                    'Class': "UScriptClass'AnimNotify_PlayParticleEffect'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'PSTemplate': {'ObjectName': "ParticleSystem'PS_JungleAbominationLand'",
                                                  'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/PS_JungleAbominationLand.61'},
                                   'LocationOffset': {'X': 0.0, 'Y': 500.0, 'Z': 0.0},
                                   'Scale': {'X': 3.0, 'Y': 3.0, 'Z': 3.0}}},
  'notify_object_sha256': 'b8734a1ed479fdd064dcea4e2cd5e5142e2ed0c68072b566e036fa02755ee2da'},
 {'clip': 'jungleAbomination_summon',
  'source_animation_sha256': 'b1f2a8de604442249679d1df211a5860c963133d7d14ae93f0e0a48194bd7991',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_summon:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_summon.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_summon',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Sum.DLC_Mob_Abom_Sum',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '545f9bebfae54133a61743a5d7cb608ffc0400e8b86cfb621c2196745b6390ca'},
 {'clip': 'jungleAbomination_summon',
  'source_animation_sha256': 'b1f2a8de604442249679d1df211a5860c963133d7d14ae93f0e0a48194bd7991',
  'time': 0.632495,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_summon:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_summon.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_summon',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Sum.DLC_Mob_Abom_V_Sum',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '0e10ce8b901fab8589f9550758bbca68af62ebbcc6982af5e256955bc5e9b6cc'},
 {'clip': 'jungleAbomination_vineAttack',
  'source_animation_sha256': '00bcf5d5073d062691fd1e8760185388b3aa676693101b8789f8b69f8cc8fc32',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttack:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttack.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_vineAttack',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAtt.DLC_Mob_Abom_VineAtt',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '82d492ca4c36882e7f414334b1ae095bc3ef828979ab049c0c6830abc5f9db7b'},
 {'clip': 'jungleAbomination_vineAttack',
  'source_animation_sha256': '00bcf5d5073d062691fd1e8760185388b3aa676693101b8789f8b69f8cc8fc32',
  'time': 1.0380974,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttack:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttack.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_vineAttack',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAtt.DLC_Mob_Abom_V_VineAtt',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '75f1b49169a3535c68fd60f75844c8e189bd77ec67302abe003d97d274014d83'},
 {'clip': 'jungleAbomination_vineAttackSucessful',
  'source_animation_sha256': 'c9ce581a79be64289b630ea260bc56bb57e358276174817b4b267bd38816bd3b',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttackSucessful:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackSucessful.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_vineAttackSucessful',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAttSucc.DLC_Mob_Abom_VineAttSucc',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '4f62240c67015adcdb5c4d9302d405de02c6e16e7bc980ba1b0cc90035fe42a7'},
 {'clip': 'jungleAbomination_vineAttackSucessful',
  'source_animation_sha256': 'c9ce581a79be64289b630ea260bc56bb57e358276174817b4b267bd38816bd3b',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttackSucessful:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackSucessful.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_vineAttackSucessful',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAttSucc.DLC_Mob_Abom_V_VineAttSucc',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '5f86a613d2c69a64dfdcd35fb22dfc05d52764cd6b53babe4190a96b98b33e2c'},
 {'clip': 'jungleAbomination_vineAttackUnsucessful',
  'source_animation_sha256': 'd62960efc4ba1f604b4b3800c227036fcb4d01270f5f0597492f2e5bb88868b8',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttackUnsucessful:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackUnsucessful.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_vineAttackUnsucessful',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAttSucc.DLC_Mob_Abom_VineAttSucc',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '567940e319ea40310a7f3dde190844a9d2678e113c502c745836cdece10740b6'},
 {'clip': 'jungleAbomination_vineAttackUnsucessful',
  'source_animation_sha256': 'd62960efc4ba1f604b4b3800c227036fcb4d01270f5f0597492f2e5bb88868b8',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vineAttackUnsucessful:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vineAttackUnsucessful.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_vineAttackUnsucessful',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAttFail.DLC_Mob_Abom_V_VineAttFail',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'b4832af088a5a6f5bad12cfb88c6a5118d3d126b6dd800d6c1ad3b65d5dfd0be'},
 {'clip': 'jungleAbomination_vulnerableFall',
  'source_animation_sha256': '8b54429c1babc1f07e8eb19aba25eceb191256e77beac9334f1a63745849e0b2',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableFall:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableFall.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_vulnerableFall',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VunFall.DLC_Mob_Abom_VunFall',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '8554eb2fc66a1bf1d120c1b25dcaff79a6a8f7f95a43de5fd61672253c135ac3'},
 {'clip': 'jungleAbomination_vulnerableFall',
  'source_animation_sha256': '8b54429c1babc1f07e8eb19aba25eceb191256e77beac9334f1a63745849e0b2',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableFall:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableFall.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_vulnerableFall',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VunFall.DLC_Mob_Abom_V_VunFall',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '2fe04a6dc50ef38b517922488a43291c81154163061d3946be90e83f66497962'},
 {'clip': 'jungleAbomination_vulnerableFall',
  'source_animation_sha256': '8b54429c1babc1f07e8eb19aba25eceb191256e77beac9334f1a63745849e0b2',
  'time': 0.78448987,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableFall:AnimNotify_DungeonsPlaySound_2'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableFall.2'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_2',
                    'Outer': 'jungleAbomination_vulnerableFall',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_FlowerOpen.DLC_Mob_Abom_FlowerOpen',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '01f831572bdc299277c4fb7883f4351f904012c7feb36e68491c8d6ac94867e1'},
 {'clip': 'jungleAbomination_vulnerableFall',
  'source_animation_sha256': '8b54429c1babc1f07e8eb19aba25eceb191256e77beac9334f1a63745849e0b2',
  'time': 0.78448987,
  'offset': 0.0,
  'notify_name': 'Trigger Flower LOOP',
  'notify': None},
 {'clip': 'jungleAbomination_vulnerableGetUp',
  'source_animation_sha256': '6190b7ccbe47da29fb6557eb0a5db6f6a071549519f680934862704aabbea13e',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableGetUp:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableGetUp.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_vulnerableGetUp',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Vun_GetUp.DLC_Mob_Abom_Vun_Getup',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'dafe5f170e990700563e11dbba76af5f3a89351bd415b3f0a25ec9f59d79a46b'},
 {'clip': 'jungleAbomination_vulnerableGetUp',
  'source_animation_sha256': '6190b7ccbe47da29fb6557eb0a5db6f6a071549519f680934862704aabbea13e',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableGetUp:AnimNotify_DungeonsPlaySound_2'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableGetUp.2'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_2',
                    'Outer': 'jungleAbomination_vulnerableGetUp',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_FlowerClose.DLC_Mob_Abom_FlowerClose',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '0be66c0ec5460d77908d6a5d66365a12741c5c40c0591d5de006b44d1e213616'},
 {'clip': 'jungleAbomination_vulnerableGetUp',
  'source_animation_sha256': '6190b7ccbe47da29fb6557eb0a5db6f6a071549519f680934862704aabbea13e',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'Flower LOOP Fade Out',
  'notify': None},
 {'clip': 'jungleAbomination_vulnerableGetUp',
  'source_animation_sha256': '6190b7ccbe47da29fb6557eb0a5db6f6a071549519f680934862704aabbea13e',
  'time': 0.3179052,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_vulnerableGetUp:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_vulnerableGetUp.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_vulnerableGetUp',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Vun_Getup.DLC_Mob_Abom_V_Vun_Getup',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'eb4f4a1c9548662a05157ab19345b92fbf27326eb5383889d3d3975b1b203e52'},
 {'clip': 'jungleAbomination_walk',
  'source_animation_sha256': 'c06f68278c3bfa90350480466d36e839d48bef0b332f6a49c5c7968e38884c59',
  'time': 0.0,
  'offset': 0.0001,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_walk:AnimNotify_DungeonsPlaySound_1'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.1'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_1',
                    'Outer': 'jungleAbomination_walk',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Walk.DLC_Mob_Abom_Walk',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '1f87584de0190d4dbce639d4f28656d3462e58651f1b6857790196685d1d796f'},
 {'clip': 'jungleAbomination_walk',
  'source_animation_sha256': 'c06f68278c3bfa90350480466d36e839d48bef0b332f6a49c5c7968e38884c59',
  'time': 0.04320923,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_walk:AnimNotify_DungeonsPlaySound_4'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.3'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_4',
                    'Outer': 'jungleAbomination_walk',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Walk.DLC_Mob_Abom_V_Walk',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '76565e55aaecb2713f331175810470759254e20d2b040e3e29c84dc29b87f601'},
 {'clip': 'jungleAbomination_walk',
  'source_animation_sha256': 'c06f68278c3bfa90350480466d36e839d48bef0b332f6a49c5c7968e38884c59',
  'time': 1.2404281,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_walk:AnimNotify_DungeonsPlaySound_0'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.0'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_0',
                    'Outer': 'jungleAbomination_walk',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Walk.DLC_Mob_Abom_Walk',
                                             'SubPathString': ''}}},
  'notify_object_sha256': '9fb449340893c2524cf083f33bb138ae81c3adcaebd303545d5a527f62a57552'},
 {'clip': 'jungleAbomination_walk',
  'source_animation_sha256': 'c06f68278c3bfa90350480466d36e839d48bef0b332f6a49c5c7968e38884c59',
  'time': 1.2918868,
  'offset': 0.0,
  'notify_name': 'DungeonsPlaySound',
  'notify': {'ObjectName': "AnimNotify_DungeonsPlaySound'jungleAbomination_walk:AnimNotify_DungeonsPlaySound_2'",
             'ObjectPath': 'Dungeons/Content/Actors/Characters/Enemies/JungleAbomination/Animation/jungleAbomination_walk.2'},
  'notify_object': {'Type': 'AnimNotify_DungeonsPlaySound',
                    'Name': 'AnimNotify_DungeonsPlaySound_2',
                    'Outer': 'jungleAbomination_walk',
                    'Class': "UScriptClass'AnimNotify_DungeonsPlaySound'",
                    'Flags': 'RF_Transactional | RF_WasLoaded | RF_LoadCompleted',
                    'Properties': {'Sound': {'AssetPathName': '/Game/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Walk.DLC_Mob_Abom_V_Walk',
                                             'SubPathString': ''}}},
  'notify_object_sha256': 'dde82f7cef231720f6806c318f9cb039294e8e085c23d78519c09df71781bd03'}]


COOKED_CUES = {'dlc_mob_abom_arenaintro': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_ArenaIntro.uasset',
                             'wave_files': ['DLC_Mob_Abom_Intro_Foley_STEREO.ogg', 'DLC_Mob_Abom_Intro_Vocal_STEREO.ogg'],
                             'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3},
                                            {'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                             'random_weights': [],
                             'uobject_sha256': {'DLC_Mob_Abom_ArenaIntro.uobject.json': '883917e0d1660b8c6fa3136aa9adc5c120d3a370f9ceb32a1f44443e0e907580',
                                                'SoundNodeMixer_0.uobject.json': 'a539f802697a69a80fc5f057a2aca37f04fce8836e7afb9e96afcc53a1db1007',
                                                'SoundNodeModulator_0.uobject.json': 'af1227db0e34c41db7710e666ba8e96339964924eb2fcdc362937e3fa028706e',
                                                'SoundNodeModulator_1.uobject.json': '183f8d55872bac5babed7f6285d454d96c468250d3bd9022c894662d357be1b7',
                                                'SoundNodeWavePlayer_0.uobject.json': 'ecaff491d59ae85a8757b8a8a4dac4d0ec8b4b99b67a079e237fd1ea49202a31',
                                                'SoundNodeWavePlayer_1.uobject.json': '05a7958b403c94361955c52a7fc83294f481fd0702f1d154432e2b8e5ce97cf7'}},
 'dlc_mob_abom_basicatt': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_BasicAtt.uasset',
                           'wave_files': ['DLC_Mob_Abom_BasicAttack_Foley.ogg'],
                           'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                           'random_weights': [],
                           'uobject_sha256': {'DLC_Mob_Abom_BasicAtt.uobject.json': '19a5415b7898989c0790894d24440a62c2bc55a86bdbbf1baf36e2c84f636013',
                                              'SoundNodeModulator_0.uobject.json': 'e968f6c16a16e5f343be6da21050e4efc4eb7eeb9b20c392cd5c9fe322884866',
                                              'SoundNodeWavePlayer_0.uobject.json': '0300988cb7cd30fdb7334274ea625b5b3e1241471fac66551e7c75d0c5b1a581'}},
 'dlc_mob_abom_death': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Death.uasset',
                        'wave_files': ['DLC_Mob_Abom_Death_Foley.ogg'],
                        'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                        'random_weights': [],
                        'uobject_sha256': {'DLC_Mob_Abom_Death.uobject.json': 'bfcdd7432d3af9a7f0d9c748f39e98496fc2f25be0ddaed7f301eaf2c5553804',
                                           'SoundNodeModulator_0.uobject.json': 'e38d8090402da1713b10e2752847c143b130ccdc75a964a8e2d08297ceed5034',
                                           'SoundNodeWavePlayer_0.uobject.json': '61c5e5d4102abbe94703001bcb632bd7572d25b255c9df2290da7fdd63b6288a'}},
 'dlc_mob_abom_flowerclose': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_FlowerClose.uasset',
                              'wave_files': ['DLC_Mob_Abom_FlowerClose.ogg'],
                              'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                              'random_weights': [],
                              'uobject_sha256': {'DLC_Mob_Abom_FlowerClose.uobject.json': '1823ac4e49284c49425068bd2426849632c28db74c50c4ddda00faffa983ca53',
                                                 'SoundNodeModulator_0.uobject.json': '73809ddcb989cccf9bb3b5136b9873c9c6cd929063a33e3c7cd362342dcd0bc2',
                                                 'SoundNodeWavePlayer_0.uobject.json': '6deea0522388be839253c5955004491846a4b2f163cd5c099ff7788758ae9173'}},
 'dlc_mob_abom_floweropen': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_FlowerOpen.uasset',
                             'wave_files': ['DLC_Mob_Abom_FlowerOpen.ogg'],
                             'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                             'random_weights': [],
                             'uobject_sha256': {'DLC_Mob_Abom_FlowerOpen.uobject.json': '1add3d94807946fc4a87597200ac774153dd18531b25a9d62cb22d0340fcae2a',
                                                'SoundNodeModulator_0.uobject.json': '5390e9980dde3e7fd45640a9becf7fd1d9ca15b2d7db6397f008b8056ca390e9',
                                                'SoundNodeWavePlayer_0.uobject.json': '87afed7e17a6ca275d47e79eda9cd31447a4860a13a0fc13f1e2a30ca5dc7b8d'}},
 'dlc_mob_abom_flower_loop': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Flower_LOOP.uasset',
                              'wave_files': [],
                              'modulators': [],
                              'random_weights': [],
                              'uobject_sha256': {'DLC_Mob_Abom_Flower_LOOP.uobject.json': '21412bad09200b6e3741278e5e86b5413781e52cc20f83a74c44e3d6858ad4fa'}},
 'dlc_mob_abom_gethit': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_GetHit.uasset',
                         'wave_files': ['DLC_Mob_Abom_GetHit1_Foley.ogg',
                                        'DLC_Mob_Abom_GetHit2_Foley.ogg',
                                        'DLC_Mob_Abom_GetHit3_Foley.ogg'],
                         'modulators': [{'PitchMin': 0.8, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                         'random_weights': [1.0, 1.0, 1.0],
                         'uobject_sha256': {'DLC_Mob_Abom_GetHit.uobject.json': '0acdf2c8501f742c61c09847db9b1756a6a8d33e657622f19bb83873a69278ea',
                                            'SoundNodeModulator_0.uobject.json': '88366dc6efabc3d7384c5a91280bd04afbd9e5d56c2b6d3936185af9d234b32c',
                                            'SoundNodeRandom_0.uobject.json': '249c0e792c92d0d09f5feb5f3eec41df32979b344417a0c1c2fdf2dea544678e',
                                            'SoundNodeWavePlayer_0.uobject.json': 'b1ee6a17fad9e5916115d810ad18e7ff1c7a2f2e84794e216fdd1b04b9237e10',
                                            'SoundNodeWavePlayer_1.uobject.json': 'edd7000e5f452d7d0b886008ef47e24024d099ec5274c47979eb0b3a7d5dc7a8',
                                            'SoundNodeWavePlayer_2.uobject.json': 'f389044437e9ed0bdff26ecfa03e038e2bced233d08e6f7f19284d006de412bb'}},
 'dlc_mob_abom_idle': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Idle.uasset',
                       'wave_files': ['DLC_Mob_Abom_Idle_Foley.ogg'],
                       'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 0.0, 'VolumeMax': 0.0}],
                       'random_weights': [],
                       'uobject_sha256': {'DLC_Mob_Abom_Idle.uobject.json': '0b58bbd4204280df474e4d2e8530d0a2928ab55f0ba19b484889bede89fea43a',
                                          'SoundNodeModulator_0.uobject.json': '1be5684aec256ee70b80f64148baa26bcdd9e49728d6bb3c8e7884c3afeb0ff8',
                                          'SoundNodeWavePlayer_0.uobject.json': 'aea8e1d8e4e5811c4e3a7eb2c6d04aeab5ce5905fc0edfebe12afdb633535a29'}},
 'dlc_mob_abom_land': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Land.uasset',
                       'wave_files': ['DLC_Mob_Abom_Land_Foley.ogg'],
                       'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                       'random_weights': [],
                       'uobject_sha256': {'DLC_Mob_Abom_Land.uobject.json': 'effd090ad26b54098abfbffb89bafcb678484779a49ff5d166e1c06985835998',
                                          'SoundNodeModulator_0.uobject.json': '5cfe9e507b4bc042281c00a7e95d8ddb53cd53f5441c772cdcfdc4e9b45148f2',
                                          'SoundNodeWavePlayer_0.uobject.json': '1a6b08718609ac5442f844bf148238e1025285be2e9c19b99f1b7e9bbc5c8863'}},
 'dlc_mob_abom_laugh': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Laugh.uasset',
                        'wave_files': ['DLC_Mob_Abom_Laugh_Vocal_STEREO.ogg'],
                        'modulators': [{'PitchMin': 0.9, 'PitchMax': 0.95, 'VolumeMin': 0.7, 'VolumeMax': 0.7}],
                        'random_weights': [],
                        'uobject_sha256': {'DLC_Mob_Abom_Laugh.uobject.json': 'f34fd038cc0e62ae7a4fa499593e89c37864ca6f59f8239234f357b111bbc439',
                                           'SoundNodeModulator_0.uobject.json': 'b5f14892735bff11f2aa2dbcd9a719efe1b282ffbc11713997cba1b301b3b313',
                                           'SoundNodeWavePlayer_3.uobject.json': '2be037fea8cda55997f48147cc217d3f40d78d9e604e000a9a92802631eb28cd'}},
 'dlc_mob_abom_sum': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Sum.uasset',
                      'wave_files': ['DLC_Mob_Abom_Summon_Foley.ogg'],
                      'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                      'random_weights': [],
                      'uobject_sha256': {'DLC_Mob_Abom_Sum.uobject.json': '88147f8f4c633f23062b91bfd9817e9354ac74e4d543bf0c31e239647e49903d',
                                         'SoundNodeModulator_0.uobject.json': '7c37713a7aedefc79eac75263f9cd1ffd296523d4603a847cc05d26d3fa38909',
                                         'SoundNodeWavePlayer_0.uobject.json': '7ec9a36fb72a38d6f59ea7393d817b780b72e304a18ffdd62d59e837a45f6a14'}},
 'dlc_mob_abom_vineatt': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAtt.uasset',
                          'wave_files': ['DLC_Mob_Abom_VineAttack_Foley.ogg'],
                          'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                          'random_weights': [],
                          'uobject_sha256': {'DLC_Mob_Abom_VineAtt.uobject.json': 'a5b594da30af4f47fb377998075a87c19a2c3929b98a220923e95d0e7ef7700a',
                                             'SoundNodeModulator_0.uobject.json': '3ec61461747bd630a66d5cfa3893c85bdbdd1b9fb2a7826de11facd6ec45a0f2',
                                             'SoundNodeWavePlayer_0.uobject.json': 'c338a6bc98d735bbd942caad69ad6ecf5e7fd9a9b44d69076d5b29f153259b3f'}},
 'dlc_mob_abom_vineattfail': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAttFail.uasset',
                              'wave_files': ['DLC_Mob_Abom_VineAttackFail_Foley.ogg'],
                              'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                              'random_weights': [],
                              'uobject_sha256': {'DLC_Mob_Abom_VineAttFail.uobject.json': '9e50f66b5e6f411e5197cdb018c0990925f41fd6df0e7833884b55215091ad0b',
                                                 'SoundNodeModulator_0.uobject.json': '999edcccb8650746a2cbcc0a7757c929a13a15a98dda8f8206af25e34895e66e',
                                                 'SoundNodeWavePlayer_0.uobject.json': '3f343900d2ce99dbb24433e1bf09c22fe117efdb1a2a3a7ebde33e856038d242'}},
 'dlc_mob_abom_vineattsucc': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VineAttSucc.uasset',
                              'wave_files': ['DLC_Mob_Abom_VineAttackSuccess_Foley.ogg'],
                              'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                              'random_weights': [],
                              'uobject_sha256': {'DLC_Mob_Abom_VineAttSucc.uobject.json': '6cfdc0355ee619cf0d7d946860f1a6e62d1ddfb5a826bf0e47eb8b94fd2def80',
                                                 'SoundNodeModulator_0.uobject.json': '2621267511927ec80a9f72ef23277feb30d9fb4e9aa5994ac397aeeba40870eb',
                                                 'SoundNodeWavePlayer_0.uobject.json': 'cc22a03bdaef56f8bfa60a03b6595218a551d05eb0366066d684cad9bd9fa562'}},
 'dlc_mob_abom_vunfall': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_VunFall.uasset',
                          'wave_files': ['DLC_Mob_Abom_Fall_Foley.ogg'],
                          'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                          'random_weights': [],
                          'uobject_sha256': {'DLC_Mob_Abom_VunFall.uobject.json': '351e58a3b6062935e78726842664169b0295eb623d5271c0535cddbe5717deb1',
                                             'SoundNodeModulator_0.uobject.json': '10935c6ad1bc77870f28b34998e7cf502d7cd3f8464fbd1a9208a7324b920c3b',
                                             'SoundNodeWavePlayer_0.uobject.json': 'e53e61fd74069218880a50666313cbd8bb46ed32ea154348d846958ce245ee0d'}},
 'dlc_mob_abom_vun_getup': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Vun_GetUp.uasset',
                            'wave_files': ['DLC_Mob_Abom_GetUp_Foley.ogg'],
                            'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                            'random_weights': [],
                            'uobject_sha256': {'DLC_Mob_Abom_Vun_Getup.uobject.json': '0f6eeb0dec878ffc956fc4b1203eb409bb33a97de887e15cab1d0d1f15fa4266',
                                               'SoundNodeModulator_0.uobject.json': '1bdba4b1d72c6e0326cba4fb742d2362359937336a6f8cbb7d8f3447a65e1cbe',
                                               'SoundNodeWavePlayer_0.uobject.json': '79878902edff9780598e2053e51a91244a47bf6b93bcd6aee36b30bf1f38a176'}},
 'dlc_mob_abom_v_basicatt': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_BasicAtt.uasset',
                             'wave_files': ['DLC_Mob_Abom_BasicAttack_Vocal.ogg',
                                            'DLC_Mob_Abom_BasicAttack2_Vocal.ogg',
                                            'DLC_Mob_Abom_VineAttack_Vocal.ogg'],
                             'modulators': [{'PitchMin': 0.92, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                             'random_weights': [1.0, 1.0, 1.0],
                             'uobject_sha256': {'DLC_Mob_Abom_V_BasicAtt.uobject.json': '4f2d7b1ca0bccf821a913fd4e7d7dc324f93e64a818232f8932bdd74e19a70e7',
                                                'SoundNodeModulator_0.uobject.json': 'f5b8f037904482618cc5916f26df93828b5cb7025eb3406da8fa5162b882cf28',
                                                'SoundNodeRandom_0.uobject.json': 'e6a0c6ddee54ab4fc5ffe42d48553d8fcfa3b79e37880004013000a5d4e216b6',
                                                'SoundNodeWavePlayer_0.uobject.json': '3b63a5d01b8ccd5cb953d4c254429796cd7c04f0431122da1640fd21f8da130d',
                                                'SoundNodeWavePlayer_1.uobject.json': 'bdfa0bd0b7bee154a1d9f1e4efd2e4ba9f7aee5f53f8b39debb86689c92f0e25',
                                                'SoundNodeWavePlayer_2.uobject.json': '09af91d4a228fd8a7a6bb402272f2f04c41593014692aeb66fe1e5d346fd9581'}},
 'dlc_mob_abom_v_death': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Death.uasset',
                          'wave_files': ['DLC_Mob_Abom_Death_Vocal.ogg'],
                          'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.35, 'VolumeMax': 1.35}],
                          'random_weights': [],
                          'uobject_sha256': {'DLC_Mob_Abom_V_Death.uobject.json': '8be155abfd8f38bc5fae5a8dd8e81f262c01029bed7b47a6967b5db184c05f47',
                                             'SoundNodeModulator_0.uobject.json': '916dc07c742b5430840e4ac448955cabdd12a168b7666135f5864725866ab7a9',
                                             'SoundNodeWavePlayer_0.uobject.json': '8f94995ef28b90f7a6ed5a35b3d8c0c5f48ea4a049ddda13b8e824438721daa2'}},
 'dlc_mob_abom_v_gethit': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_GetHit.uasset',
                           'wave_files': ['DLC_Mob_Abom_GetHit1_Vocal.ogg',
                                          'DLC_Mob_Abom_GetHit2_Vocal.ogg',
                                          'DLC_Mob_Abom_GetHit3_Vocal.ogg',
                                          'DLC_Mob_Abom_GetHit4_Vocal.ogg'],
                           'modulators': [{'PitchMin': 0.92, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                           'random_weights': [1.0, 1.0, 1.0, 1.0],
                           'uobject_sha256': {'DLC_Mob_Abom_V_GetHit.uobject.json': '581501743aa6c1f42fcb7e99740bd32cc7a3b23d9ffeac86478b95231563b414',
                                              'SoundNodeModulator_0.uobject.json': '81c2a23c9373f53385066014dc214fea2143cb8be5f729d22ebcf5c5a8ce8992',
                                              'SoundNodeRandom_0.uobject.json': 'd34abf55e70cbce1f18e7af433d7bafa852907e502a3f7eef91cd712ade0da14',
                                              'SoundNodeWavePlayer_0.uobject.json': '0e45481151945d972e4ba00cb2e46855bcf13afd3a592c0d27cba150a182ad43',
                                              'SoundNodeWavePlayer_1.uobject.json': 'a4ab599d148ce6be1faab43165e7adc268dec8f730db58a321d2a40cc6265457',
                                              'SoundNodeWavePlayer_2.uobject.json': 'ca5b28d551d0008f7aaf6d994d1feeb717b55f488aba41ddc1dc374255822b99',
                                              'SoundNodeWavePlayer_3.uobject.json': '64800540065395cdcfd80d17dabfa40247adb6d664b296f95892fd32c3aae148'}},
 'dlc_mob_abom_v_idle': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Idle.uasset',
                         'wave_files': ['DLC_Mob_Abom_Idle_Vocal.ogg'],
                         'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 0.0, 'VolumeMax': 0.0}],
                         'random_weights': [],
                         'uobject_sha256': {'DLC_Mob_Abom_V_Idle.uobject.json': 'b270cfb76ced32f0be6bc2a4b7851215ca4caf80e489a58b21eba263898b8e55',
                                            'SoundNodeModulator_0.uobject.json': '65331876f7e33547c7228d61a15b375197980a92e921e583bee6a8dd25af1515',
                                            'SoundNodeWavePlayer_0.uobject.json': '3a71dab8b2a2d3f07062519d46b5d6c334afbb0034d7e4b1cd2dc70a9261e3cb'}},
 'dlc_mob_abom_v_land': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Land.uasset',
                         'wave_files': ['DLC_Mob_Abom_Land_Vocal.ogg'],
                         'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                         'random_weights': [],
                         'uobject_sha256': {'DLC_Mob_Abom_V_Land.uobject.json': '72591771f1fd3febb2205cef69fc40adc650df5dbd2ff56a922ae2ff07b66aee',
                                            'SoundNodeModulator_0.uobject.json': '0f128373aaf2289c99d1a3b1f42f70220bf5fb95a13c711b0278a8aa4a68b4e3',
                                            'SoundNodeWavePlayer_0.uobject.json': 'c9e850588088c5feef6b0ba9c794d6539184ae51aa270af44139e43942f649ef'}},
 'dlc_mob_abom_v_sum': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Sum.uasset',
                        'wave_files': ['DLC_Mob_Abom_Summon_Vocal.ogg'],
                        'modulators': [{'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                        'random_weights': [],
                        'uobject_sha256': {'DLC_Mob_Abom_V_Sum.uobject.json': '9b97cf236539920f25ff85d617b1e4ebaec86d42c74291f37ad283341bfc0d16',
                                           'SoundNodeModulator_0.uobject.json': 'ce0ccbcf7bf942c1a83881ed026c7b15c7b6896fa34c019dfbc3bedc4600f8d3',
                                           'SoundNodeWavePlayer_0.uobject.json': '66f1d3d8e3662ec144ccc55816bbcd37e3ae4f55e56263282047c2a0248439e0'}},
 'dlc_mob_abom_v_vineatt': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAtt.uasset',
                            'wave_files': ['DLC_Mob_Abom_VineAttack_Vocal.ogg',
                                           'DLC_Mob_Abom_BasicAttack_Vocal.ogg',
                                           'DLC_Mob_Abom_BasicAttack2_Vocal.ogg'],
                            'modulators': [{'PitchMin': 0.92, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                            'random_weights': [1.0, 1.0, 1.0],
                            'uobject_sha256': {'DLC_Mob_Abom_V_VineAtt.uobject.json': '69623abaa7c37e1e80859488035a083f20f778841a7b49946e9dd80e4007cfce',
                                               'SoundNodeModulator_0.uobject.json': '51e1230fa2505c52327f91ecadde0e80270a2bb6a9a23a892f72dc32c310749b',
                                               'SoundNodeRandom_0.uobject.json': 'af5f4f5b1924772896ababdf37d236002807801d180007ac0307d9026615d795',
                                               'SoundNodeWavePlayer_0.uobject.json': '4c753566bb295da1b934f85cb587819e1d924d6538ca9b9d2ad9e9219161aa14',
                                               'SoundNodeWavePlayer_1.uobject.json': 'cc508a7c78563d65f7474fbbee3993991aed1a9bead2cc0640f9548c15c95b48',
                                               'SoundNodeWavePlayer_2.uobject.json': '85cc41f833fd65a0e852844fb09ec713bddcf7a097eb34194f4dbe3f804e5543'}},
 'dlc_mob_abom_v_vineattfail': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAttFail.uasset',
                                'wave_files': ['DLC_Mob_Abom_VineAttackFail_Vocal.ogg'],
                                'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.15, 'VolumeMax': 1.15}],
                                'random_weights': [],
                                'uobject_sha256': {'DLC_Mob_Abom_V_VineAttFail.uobject.json': 'ed278a52f4d5e6f664961b092d010b750545126602d9cf78ea3875be54119f32',
                                                   'SoundNodeModulator_0.uobject.json': '204f698eacc52cfd84da1c53a66d401f3298813d728635b0440ff5379e4bd531',
                                                   'SoundNodeWavePlayer_0.uobject.json': '638557dfcea6f1ff0b0789860ccce64b6705c971d95238f8d43425512b233db0'}},
 'dlc_mob_abom_v_vineattsucc': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VineAttSucc.uasset',
                                'wave_files': ['DLC_Mob_Abom_VineAttackSuccess_Vocal.ogg'],
                                'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                                'random_weights': [],
                                'uobject_sha256': {'DLC_Mob_Abom_V_VineAttSucc.uobject.json': 'c92d75e5bc7ef65478f9a2705d68c8af66ee56f196933c3ae7ca07338ed02cf5',
                                                   'SoundNodeModulator_0.uobject.json': 'f269cfa16c6bb1970b52a7d0013ab87e6f3edeb93aa6fd50fa09b46d05727f34',
                                                   'SoundNodeWavePlayer_0.uobject.json': 'ec86ad49140440001bfc0b9d296025bfa82955f4277f1cf1103067c29b37bf13'}},
 'dlc_mob_abom_v_vunfall': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_VunFall.uasset',
                            'wave_files': ['DLC_Mob_Abom_Fall_Vocal.ogg'],
                            'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                            'random_weights': [],
                            'uobject_sha256': {'DLC_Mob_Abom_V_VunFall.uobject.json': '81e230ca30009dfc37d36e2428c8199485bdd7966474ee9affa13b196c4a4de0',
                                               'SoundNodeModulator_0.uobject.json': 'eb693402dd896b10e46b8a3587748a62b3741b00c57f74fa581f899b11ce20b4',
                                               'SoundNodeWavePlayer_0.uobject.json': '03b5b168bfddb15a7a3e8ad99bf0124a5d1c38cab14a3abc3763d28abb9c47ca'}},
 'dlc_mob_abom_v_vun_getup': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Vun_Getup.uasset',
                              'wave_files': ['DLC_Mob_Abom_GetUp_Vocal.ogg'],
                              'modulators': [{'PitchMin': 1.0, 'PitchMax': 1.0, 'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                              'random_weights': [],
                              'uobject_sha256': {'DLC_Mob_Abom_V_Vun_Getup.uobject.json': '60cc08e43c4c4b8e1b3543e1e80e2340b2fbf903e3e1724c8c3052e2e06775f1',
                                                 'SoundNodeModulator_0.uobject.json': 'e106c4278e8dfe6a45c863bb7b9d385cf0579c716dfa59ec3d7456e7fe5b2091',
                                                 'SoundNodeWavePlayer_0.uobject.json': '5c7ba83cb2a5a930dd49ab6046e4cacea77e354bd68b239fec549e65a07ded75'}},
 'dlc_mob_abom_v_walk': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_V_Walk.uasset',
                         'wave_files': ['DLC_Mob_Abom_Walk1_Vocal.ogg', 'DLC_Mob_Abom_Walk2_Vocal.ogg', None, None],
                         'modulators': [{'VolumeMin': 1.0, 'VolumeMax': 1.0}],
                         'random_weights': [1.0, 1.0, 1.0, 1.0],
                         'uobject_sha256': {'DLC_Mob_Abom_V_Walk.uobject.json': 'f37d7b1b85e469bdb66db857b0bd081a3810317615db74762cb3fe7e19db4146',
                                            'SoundNodeModulator_0.uobject.json': 'd515008f9c6868b39b451612866cd35c89fc889b7749cf9085cf4b70fde7a976',
                                            'SoundNodeRandom_0.uobject.json': '81035983cfe5a8b60b05bbd87910916595fa35b6eaf9c48cd712ae727590089b',
                                            'SoundNodeWavePlayer_0.uobject.json': 'fae9629f009417d6d1355c0be0efc4c55f5b112d550bcdd55cc1863d9c902953',
                                            'SoundNodeWavePlayer_1.uobject.json': '644cdd8e668fe1701e320297e4e7ecae69737d945914f52c9c7021018e807a6d',
                                            'SoundNodeWavePlayer_2.uobject.json': 'b588819dff21091ae8699b9e11cb2e06fdee3b1611f9ab08a72c23f56f8f1825',
                                            'SoundNodeWavePlayer_3.uobject.json': 'f0706b325519ec264b2852c33b254c997f114bba78116887dad7e800f9e9f787'}},
 'dlc_mob_abom_walk': {'source_package': 'Dungeons/Content/AudioForce/DLC_audio/DLC_Mob_soundCue/Jungle_Abomination/DLC_Mob_Abom_Walk.uasset',
                       'wave_files': ['DLC_Mob_Abom_Walk1_Foley.ogg', 'DLC_Mob_Abom_Walk2_Foley.ogg'],
                       'modulators': [{'PitchMin': 0.9, 'VolumeMin': 1.3, 'VolumeMax': 1.3}],
                       'random_weights': [1.0, 1.0],
                       'uobject_sha256': {'DLC_Mob_Abom_Walk.uobject.json': 'e9fee7f1bb3f0412ff4c17c7f69b9ed0e13a7616da56f7a2bbca646ea884a92c',
                                          'SoundNodeModulator_0.uobject.json': 'ee36b576637a1db802e2be41a2ce9c42ec68edeec92bb7e33811999f58e364d2',
                                          'SoundNodeRandom_0.uobject.json': '97ad4a2c8d67d9d12468d45171c39b574493958983035ab7301ffce1f0553f3c',
                                          'SoundNodeWavePlayer_0.uobject.json': '707df59874b8650abbb97f03eac32560aaa17341541861686b4e1ae0fb560ebf',
                                          'SoundNodeWavePlayer_1.uobject.json': '101d6faa7e241d3f01cb94819352f5a6959b29cddbc2081184c1470cd9c1ffac'}}}


def _apply_cooked_pools():
    policies={}
    for package,event in _ASSET_EVENTS.items():
        cue=COOKED_CUES[package]
        files=[name for name in cue['wave_files'] if name is not None]
        if not files:raise ValueError('Expected nonempty SoundCue wave pool: '+package)
        subtitle,_,extra=SOUNDS[event]
        SOUNDS[event]=(subtitle,files,extra)
        modulators=cue['modulators']
        if len(modulators)!=1:raise ValueError('Expected one modulator for bound SoundCue')
        mod=modulators[0]
        volume=mod['VolumeMin'] if mod.get('VolumeMin')==mod.get('VolumeMax') else 1.
        pitch=mod['PitchMin'] if mod.get('PitchMin') is not None and mod.get('PitchMin')==mod.get('PitchMax') else 1.
        if cue['random_weights'] and any(x!=1 for x in cue['random_weights']):
            raise ValueError('Unequal source SoundCue weights require explicit conversion')
        policies[event]={'volume':volume,'pitch':pitch,
            'audible_chance':len(files)/len(cue['wave_files']),
            'source_modulator':mod,'source_wave_files':cue['wave_files'],
            'pitch_policy':'fixed source value' if mod.get('PitchMin')==mod.get('PitchMax') and 'PitchMin'in mod else'target 1; random/default source pitch not reproduced'}
    return policies


EVENT_POLICIES=_apply_cooked_pools()


def _event(row):
    sound = row.get('notify_object',{}).get('Properties',{}).get('Sound',{}).get('AssetPathName')
    if sound:
        package = sound.split('.')[0].split('/')[-1].lower()
        return _ASSET_EVENTS[package]
    if row['notify_name'] == 'Trigger Flower LOOP':
        return 'flower_loop'
    return None


def _cues():
    result = {}
    for row in SOURCE_NOTIFIES:
        event = _event(row)
        if event is not None:
            policy=EVENT_POLICIES.get(event,{'volume':1.,'pitch':1.})
            if policy['volume']==0:continue  # Two original idle cues are explicitly muted.
            at = max(0.,float(row['time'])+float(row.get('offset') or 0.))
            result.setdefault(row['clip'].lower(),[]).append((at,event,policy['volume'],policy['pitch']))
    return {name: sorted(cues) for name,cues in result.items()}


CUES = _cues()
ENTER_CUES = {}
HURT = 'hurt_voice'
HURT_FOLEY = 'hurt_foley'
DEATH = 'death_voice'
DEATH_FOLEY = 'death_foley'
# Both source idle modulators are muted. No random ambient rate is invented.
AMBIENT = None
STOP_CUES = {'jungleabomination_vulnerablegetup': [(0.,'flower_loop')]}
FLOWER_STATE = {
    'start_clip':'jungleabomination_vulnerablefall', 'start_seconds':0.78448987,
    'stop_clip':'jungleabomination_vulnerablegetup', 'stop_seconds':0.,
    'loop_clip':'jungleabomination_vulnerablestuncycle',
    'event':'flower_loop', 'sample_duration_seconds':4.325510204081633,
    'evidence':'Named source notifies Trigger Flower LOOP / Flower LOOP Fade Out; Wiki Flower_LOOP file is a semantic mapping, not a connected SoundCue wave proof.',
    'limitation':'Exported Flower_LOOP SoundCue has no FirstNode. CUES maps the named source event to one Wiki Ogg; persistent loop scheduling/fade is a target runtime policy. Do not replay every 0.875s stun cycle or globally stop another carrier sound.',
}


def configuration(ref):
    """Mob-ready mapping. Caller handles per-carrier death/fallback deduplication."""
    return dict(sounds=SOUNDS, sound_dir=str(Path(ref)/'sounds'), cues=CUES,
                enter_cues=ENTER_CUES, hurt=HURT, death=DEATH, ambient=AMBIENT,
                hurt_volume=EVENT_POLICIES[HURT]['volume'],death_volume=EVENT_POLICIES[DEATH]['volume'])


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def motion_markers(ref):
    """Diagnostic source-pose anchors, explicitly not proven sound/release times."""
    path = Path(ref)/'source/animations/jungleAbomination_ProjectileAttack.tracks.json'
    seq = json.loads(path.read_text(encoding='utf-8'))['sequences'][0]
    track = next(t for t in seq['tracks'] if t['boneName']=='Head')
    qs = track['rotation']; q0 = qs[0]
    def norm(q): return math.sqrt(sum(x*x for x in q))
    angles = [math.degrees(2*math.acos(min(1.,abs(sum(a*b for a,b in zip(q0,q))/(norm(q0)*norm(q)))))) for q in qs]
    index = max(range(len(angles)),key=angles.__getitem__)
    times = track.get('rotationTime') or track.get('time')
    frame = times[index] if times else index*seq['NumFrames']/len(qs)
    petals = {t['boneName']:len(t['rotation']) for t in seq['tracks'] if t['boneName'].startswith('J_Petal_')}
    return {'projectile_head_max_angular_displacement':{
        'source_frame_coordinate':frame,'seconds':frame/seq['FramesPerSecond'],
        'angle_degrees':angles[index],'bone':'Head','kind':'derived_pose_anchor_only',
        'method':'Maximum shortest quaternion angle relative to the first source Head key; this is not proof of projectile release or a sound notify.',
        'source_sha256':_sha(path),'audio_bound':False},
        'projectile_petal_rotation_key_counts':petals,
        'projectile_audio_policy':'No source sound notifies in full clip or its three composites; register available sounds but do not invent a projectile event from static petals or head recoil.',
        'attack_shockwave_particle': {'seconds':1.5364347,'kind':'source_particle_notify',
            'audio_bound':False,'note':'Attack_BOOM Wiki use is unverified; the particle time is an audition anchor, not proof that this audio plays here.'}}


def validate_sources(ref):
    """Read-only provenance and coverage audit; raises for missing/changed assets."""
    ref = Path(ref)
    manifest = json.loads((ref/'source/wiki_audio_manifest.json').read_text(encoding='utf-8'))
    known = {entry['filename']:entry for entry in manifest['files']}
    registered = [file for _,files,_ in SOUNDS.values() for file in files]
    if len(known)!=46 or set(registered)!=set(known):
        raise ValueError('Sound registry must cover all 44 main and 2 supplemental files')
    files = []
    for name in sorted(set(registered)):
        path = ref/'sounds'/name
        if _sha(path)!=known[name]['sha256']:
            raise ValueError('Original Ogg changed: '+name)
        files.append({'file':name,'sha256':known[name]['sha256'],'source_url':known[name]['source_url'],
                      'duration_seconds':known[name]['validation']['duration_seconds'],
                      'music_preview':known[name]['group']=='music',
                      'events':[e for e,(_,pool,_) in SOUNDS.items() if name in pool]})
    cue_rows = []
    for row in SOURCE_NOTIFIES:
        path=ref/'source/animations'/(row['clip']+'.uobject.json')
        if _sha(path)!=row['source_animation_sha256']:
            raise ValueError('Notify source changed: '+row['clip'])
        source=json.loads(path.read_text(encoding='utf-8'))['Properties'].get('Notifies',[])
        if not any(n.get('Notify')==row['notify'] and n['NotifyName']==row['notify_name']
                   and n['LinkValue']==row['time'] and n.get('TriggerTimeOffset')==row['offset'] for n in source):
            raise ValueError('Notify evidence missing from current source')
        event=_event(row)
        cue_rows.append(dict(row,event=event,at_seconds=max(0.,row['time']+(row['offset'] or 0.)),
                             muted_by_source=EVENT_POLICIES.get(event,{}).get('volume')==0,
                             timing_evidence='source_notify',time_quantization='round(seconds/0.05), then next baked sample'))
    if any(event in MUSIC_EVENTS for cues in CUES.values() for _,event,_,_ in cues):
        raise ValueError('Music must remain explicit debug-only')
    return {'status':'pass','registered_files':len(files),'main_sounds':44,'supplemental_vine':2,
            'music_previews':3,'music_default_playback':False,'registered_events':len(SOUNDS),
            'source_notify_records':len(SOURCE_NOTIFIES),'bound_timed_events':sum(map(len,CUES.values())),
            'files':files,'notifies':cue_rows,'motion_markers':motion_markers(ref),
            'flower_state':FLOWER_STATE,'hurt_policy':'Trigger on actual carrier damage; no animation time is invented.',
            'death_policy':'Death clip uses both source t=0 notifies. Orphan fallback must be suppressed if that carrier already played the death clip, and during phase undress.',
            'ambient_policy':'None: both original idle SoundCue modulators explicitly set VolumeMin=VolumeMax=0.',
            'cooked_soundcue_packages':COOKED_CUES,'event_policies':EVENT_POLICIES,
            'wiki_mapping_limit':'Source WavePlayer references prove active wave pools; equal weights preserved. Walk vocal has two empty of four branches, applied as 50% predicate. Pitch random ranges/defaults, attenuation/concurrency and no-repeat history are not fully reproduced.',
            'known_source_anomaly':'vineAttackUnsucessful source Foley references VineAttSucc; retained as source, while its vocal references VineAttFail.',
            'no_gameplay_or_summons_added':True}


def write_debug_functions(datapack, key='lucifer_p2'):
    """Explicit audition only. Never called from load/tick, no summons or loops."""
    if not re.fullmatch('[a-z0-9_]+',key):
        raise ValueError('Invalid resource key')
    folder=Path(datapack)/'data/rpg/function'/key/'debug/sound'
    folder.mkdir(parents=True,exist_ok=True)
    for event in SOUNDS:
        category='music' if event in MUSIC_EVENTS else 'hostile'
        note='Wiki music preview; not a full game soundtrack. Manual invocation only.' if event in MUSIC_EVENTS else 'Manual audition of original Wiki Ogg; no entity is summoned.'
        text=f'# {note}\nplaysound rpg:{key}.{event} {category} @a[distance=..48] ~ ~ ~ 1 1\n'
        (folder/(event+'.mcfunction')).write_text(text,encoding='utf-8')
    return {'events':len(SOUNDS),'folder':str(folder),'music_events':list(MUSIC_EVENTS)}


def finalize_runtime_sound_policies(mob):
    """After display_mob.build: retain the source walk-vocal empty branches.

    Only this mob's generated animation functions and predicate are touched.
    Idempotent; no shared code or gameplay is changed. Returns evidence counts.
    """
    chance=EVENT_POLICIES['walk_voice']['audible_chance']
    if chance!=.5:raise ValueError('Walk vocal source branch structure changed')
    path=Path(mob.dp)/'data/rpg/predicate'/mob.key/'sound/walk_voice_chance.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({'condition':'minecraft:random_chance','chance':chance},indent=2)+'\n',encoding='utf-8')
    guard=f'execute if predicate rpg:{mob.key}/sound/walk_voice_chance run '
    needle=f'playsound rpg:{mob.key}.walk_voice '
    count=0
    for function in sorted(Path(mob.anim).rglob('*.mcfunction')):
        lines=function.read_text(encoding='utf-8').splitlines();changed=False
        for index,line in enumerate(lines):
            if needle in line:
                count+=1
                if not line.startswith(guard):lines[index]=guard+line;changed=True
        if changed:function.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if count!=2:raise ValueError('Expected exactly two walk-vocal timeline cues, found '+str(count))
    return {'walk_voice_audible_chance':chance,'guarded_timeline_cues':count,
            'source_empty_branches':2,'source_total_branches':4,'predicate':str(path)}
