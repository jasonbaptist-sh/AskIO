from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["Equipment Tag", "Equipment Type", "Equipment Purpose", "Hazard", "Process", "Engineering Discipline", "Equipment Parameter"]

PROMPTS["entity_extraction"] = """---Goal---
Given a text document containing information on Prelude FLNG that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name
- entity_type: One of the following types: [{entity_types}]
- Equipment Tag: Specific identifier for a piece of equipment (e.g., K-10002 is a compressor in unit 10000, 100-UCA-1510 is a anti-surge valve in unit 10000).
- Equipment Type: The general category of equipment (e.g., Compressor, Controller, Valve, Pump, Heat Exchanger).
- Equipment Purpose: The function or role of a piece of equipment within a process (e.g., Anti-surge control, Depletion compression, Feed gas separation).
- Equipment design parameters (eg. maximum design temperature, minimum design temperature, maximum design pressure).
- Hazard: Something that if released could result in harm (e.g., hydrocarbon gas, high pressure, heat, cryogenic liquid).
- Process: A series of actions or steps taken to achieve a particular end (e.g., Surge Control, Medical Emergency Response, Management of Change).
- Engineering Discipline: A branch of engineering knowledge or practice mentioned (e.g., Process Engineering, Mechanical Engineering, Instrumentation, Process Control).
- Equipment Parameter: A measurable factor relating to equipment operation or condition (e.g., Discharge Flow, Suction Pressure, Surge Parameter, Range, Size, Capacity).
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.
Crucially, the delimiters `{tuple_delimiter}`, `{record_delimiter}`, and `{completion_delimiter}` must *only* be used for structuring the output as specified and must NEVER appear inside any extracted text field (like names, types, descriptions, or keywords).

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:
 
Entity_types: [Equipment Tag, Equipment Type, Equipment Purpose, Hazard, Process, Engineering Discipline, Equipment Parameter]
Text:
```
For the depletion compressor K-10002, dedicated anti-surge controller UCA-1510 is provided. Measurements of the discharge flow FI-1012 (Median Function FY-1012: FT-1012A/B/C), suction pressure PI-1065 (Median Function PY-1065: PT-1065A/B/C) and discharge pressure PI-1063 (Median Function PY-1063: PT-1063A/B/C) are used by the UY-1514 calculation block to compute the surge parameter, which give the distance of the K-10002 operating point from the surge reference line. At the surge reference line the surge parameter equals 10. As the K-10002 moves towards the surge control line, the anti-surge controller UCA-1510 opens the anti-surge valve UCV-1511 to move the K-10002 away from the surge reference line. Gain scheduling (UY-1516) is used to allow for both a quick opening of the anti-surge valve when getting too close to the surge reference line and stable recycle operation at the surge control line. Hand controller HC-1032 is available from the CCR to manually open the anti-surge valve UCV1511. The anti-surge controller UCA-1510 can open the anti-surge valve more, if required, through high selector UY-1513. To prevent a quick closure of the anti-surge control valve a rate of change limiter, UY-1517, is applied. This rate of change limiter only limits the closure of the valve and does not limit the speed of opening of the valve. The output signal to the anti-surge valve is inversed as the anti-surge valve is a fail-open valve.
```
 
Output:
("entity"{tuple_delimiter}"K-10002"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Depletion Compressor K-10002 is a piece of rotating equipment used in the depletion process."){record_delimiter}
("entity"{tuple_delimiter}"Depletion Compressor"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A type of compressor used specifically during the depletion phase of a gas field."){record_delimiter}
("entity"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Dedicated anti-surge controller for K-10002."){record_delimiter}
("entity"{tuple_delimiter}"Anti-surge Controller"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A controller designed to prevent compressor surge."){record_delimiter}
("entity"{tuple_delimiter}"FI-1012"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Discharge flow measurement for K-10002."){record_delimiter}
("entity"{tuple_delimiter}"Flow Instrument"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"An instrument measuring fluid flow rate."){record_delimiter}
("entity"{tuple_delimiter}"PI-1065"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Suction pressure measurement for K-10002."){record_delimiter}
("entity"{tuple_delimiter}"PI-1063"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Discharge pressure measurement for K-10002."){record_delimiter}
("entity"{tuple_delimiter}"Pressure Instrument"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"An instrument measuring fluid pressure."){record_delimiter}
("entity"{tuple_delimiter}"UCV-1511"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Anti-surge valve for K-10002."){record_delimiter}
("entity"{tuple_delimiter}"Anti-surge Valve"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A valve used in anti-surge control systems."){record_delimiter}
("entity"{tuple_delimiter}"HC-1032"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Hand controller for manually operating UCV-1511."){record_delimiter}
("entity"{tuple_delimiter}"Hand Controller"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A manual interface for controlling equipment."){record_delimiter}
("entity"{tuple_delimiter}"Surge Control"{tuple_delimiter}"Process"{tuple_delimiter}"The process of preventing compressor surge by managing operating parameters and recycle flow."){record_delimiter}
("entity"{tuple_delimiter}"Surge"{tuple_delimiter}"Hazard"{tuple_delimiter}"A condition in centrifugal compressors where flow reverses, potentially causing damage."){record_delimiter}
("entity"{tuple_delimiter}"Instrumentation"{tuple_delimiter}"Engineering Discipline"{tuple_delimiter}"The engineering discipline focused on measurement and control of process variables."){record_delimiter}
("entity"{tuple_delimiter}"Process Control"{tuple_delimiter}"Engineering Discipline"{tuple_delimiter}"The engineering discipline focused on automating and optimizing industrial processes."){record_delimiter}
("entity"{tuple_delimiter}"Surge Parameter"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"A calculated value indicating the proximity of the compressor operating point to the surge line."){record_delimiter}
("entity"{tuple_delimiter}"Discharge Flow"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The rate of fluid flow exiting the compressor discharge."){record_delimiter}
("entity"{tuple_delimiter}"Suction Pressure"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The pressure of the fluid entering the compressor suction."){record_delimiter}
("entity"{tuple_delimiter}"Discharge Pressure"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The pressure of the fluid exiting the compressor discharge."){record_delimiter}
("relationship"{tuple_delimiter}"K-10002"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"UCA-1510 is the dedicated anti-surge controller for compressor K-10002."{tuple_delimiter}"control, protection"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"UCV-1511"{tuple_delimiter}"Anti-surge controller UCA-1510 opens anti-surge valve UCV-1511 to prevent surge."{tuple_delimiter}"control action, surge prevention"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"FI-1012"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"Discharge flow measurement FI-1012 is an input to the anti-surge controller UCA-1510 for surge parameter calculation."{tuple_delimiter}"measurement input, control calculation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"PI-1065"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"Suction pressure measurement PI-1065 is an input to the anti-surge controller UCA-1510 for surge parameter calculation."{tuple_delimiter}"measurement input, control calculation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"PI-1063"{tuple_delimiter}"UCA-1510"{tuple_delimiter}"Discharge pressure measurement PI-1063 is an input to the anti-surge controller UCA-1510 for surge parameter calculation."{tuple_delimiter}"measurement input, control calculation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Surge Control"{tuple_delimiter}"K-10002"{tuple_delimiter}"Surge control process is implemented to protect the K-10002 depletion compressor."{tuple_delimiter}"process application, equipment protection"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"depletion compressor, surge control, anti-surge controller, anti-surge valve, instrumentation, process parameters"){completion_delimiter}
#############################""",
    """Example 2:
 
Entity_types: [Equipment Tag, Equipment Type, Equipment Purpose, Hazard, Process, Engineering Discipline, Equipment Parameter]
Text:
```
First Person on Scene • Assess scene and casualty • Make the area safe • Notify CCR (Central Control Room) by Radio or call Site Emergency Number 888 CCR • Dispatch Designated First Aiders (DFA) • Informs Medic of ongoing response; deploy in case of significant injury/illness DFA • Obtain first aid kit with AED. If in hazardous area, obtain authorization from IC/CCR to use AED • Mobilise to incident site • Assess IP • Provide Basic Life Support (BLS) / First Aid
```
 
Output:
("entity"{tuple_delimiter}"CCR"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Central Control Room, the main operational control hub."){record_delimiter}
("entity"{tuple_delimiter}"Central Control Room"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A facility area housing control systems and operators."){record_delimiter}
("entity"{tuple_delimiter}"Radio"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"Communication device used for notifying CCR."){record_delimiter}
("entity"{tuple_delimiter}"First Aid Kit"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A collection of supplies for giving first aid."){record_delimiter}
("entity"{tuple_delimiter}"AED"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Automatic External Defibrillator, used in Basic Life Support."){record_delimiter}
("entity"{tuple_delimiter}"Automatic External Defibrillator"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A portable electronic device that automatically diagnoses life-threatening cardiac arrhythmias and treats them through defibrillation."){record_delimiter}
("entity"{tuple_delimiter}"Medical Emergency Response"{tuple_delimiter}"Process"{tuple_delimiter}"The initial steps taken in response to a medical emergency, involving scene assessment, notification, and first aid."){record_delimiter}
("entity"{tuple_delimiter}"Injury/Illness"{tuple_delimiter}"Hazard"{tuple_delimiter}"The potential harm to personnel requiring medical attention."){record_delimiter}
("entity"{tuple_delimiter}"Hazardous Area"{tuple_delimiter}"Hazard"{tuple_delimiter}"An area with potential dangers requiring authorization for specific actions like using an AED."){record_delimiter}
("entity"{tuple_delimiter}"Basic Life Support"{tuple_delimiter}"Process"{tuple_delimiter}"A level of medical care used for victims of life-threatening illnesses or injuries until they can be given full medical care."){record_delimiter}
("entity"{tuple_delimiter}"First Aid"{tuple_delimiter}"Process"{tuple_delimiter}"Immediate assistance given to any person suffering a sudden illness or injury."){record_delimiter}
("entity"{tuple_delimiter}"Health, Safety, Environment"{tuple_delimiter}"Engineering Discipline"{tuple_delimiter}"Discipline focused on ensuring safe and environmentally sound operations, including emergency response."){record_delimiter}
("relationship"{tuple_delimiter}"First Person on Scene"{tuple_delimiter}"CCR"{tuple_delimiter}"The First Person on Scene notifies the CCR to initiate the emergency response."{tuple_delimiter}"notification, communication"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CCR"{tuple_delimiter}"DFA"{tuple_delimiter}"The CCR dispatches Designated First Aiders to the incident site."{tuple_delimiter}"dispatch, response coordination"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"DFA"{tuple_delimiter}"AED"{tuple_delimiter}"Designated First Aiders obtain and potentially use an AED as part of providing Basic Life Support."{tuple_delimiter}"equipment use, life support"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"DFA"{tuple_delimiter}"Hazardous Area"{tuple_delimiter}"Designated First Aiders require authorization to use an AED in a hazardous area."{tuple_delimiter}"safety procedure, hazard mitigation"{tuple_delimiter}5){record_delimiter}
("content_keywords"{tuple_delimiter}"medical emergency, first aid, emergency response, CCR, DFA, AED, hazardous area, basic life support"){completion_delimiter}
#############################""",
    """Example 3:
 
Entity_types: [Equipment Tag, Equipment Type, Equipment Purpose, Hazard, Process, Engineering Discipline, Equipment Parameter]
Text:
```
Not In-Kind INSTRUMENTATION Change in range of control element Different tuning parameters which affect safety or equipment integrity Changes in a loop configuration Change in a measurement type of device (e.g. orifice to mass flow meter, etc.) Different units of measurement Change to SOC, alarm limit, or interlock limit, even if limits are more stringent Changes in size of device (e.g. 4" control valve to 6" control valve) Change in Alarm Set Points Change in the functionality of SIS Equipment Change ACAP Clamp Limits outside established operating limits Relocation, decommissioning or relocation of existing equipment Introduction of new control technology Change in configuration of basic control system Introduction of new hardware/ technology (including change-over and retirement). Changing the technology associated with a Significant transmitter model changes (for example analogue to smart) Changing body types Changing the control valve capacity, characteristics, or metallurgy Disconnecting instrument air from a control valve to make it inoperable A change in the operational software that can affect plant operations, including computer control schemes
```
 
Output:
("entity"{tuple_delimiter}"Control Element"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A device that manipulates a process variable, such as a control valve."){record_delimiter}
("entity"{tuple_delimiter}"Orifice Plate"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A device used for measuring flow rate, based on differential pressure."){record_delimiter}
("entity"{tuple_delimiter}"Mass Flow Meter"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"An instrument that measures the mass flow rate of a fluid traveling through a tube."){record_delimiter}
("entity"{tuple_delimiter}"Control Valve"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A valve used to control fluid flow by varying the size of the flow passage."){record_delimiter}
("entity"{tuple_delimiter}"SIS Equipment"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"Safety Instrumented System equipment designed to prevent or mitigate hazardous events."){record_delimiter}
("entity"{tuple_delimiter}"Transmitter"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"A device that converts a measured physical variable into a standardized signal for transmission."){record_delimiter}
("entity"{tuple_delimiter}"Management of Change"{tuple_delimiter}"Process"{tuple_delimiter}"The process for handling modifications to equipment, procedures, or systems that are not 'like-for-like'."){record_delimiter}
("entity"{tuple_delimiter}"Decommissioning"{tuple_delimiter}"Process"{tuple_delimiter}"The process of taking equipment or a facility out of service."){record_delimiter}
("entity"{tuple_delimiter}"Instrumentation"{tuple_delimiter}"Engineering Discipline"{tuple_delimiter}"The discipline focused on the design, installation, and maintenance of measuring and control instruments."){record_delimiter}
("entity"{tuple_delimiter}"Process Control"{tuple_delimiter}"Engineering Discipline"{tuple_delimiter}"The discipline focused on automating and optimizing industrial processes using control systems."){record_delimiter}
("entity"{tuple_delimiter}"Range"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The upper and lower limits within which an instrument or control element operates."){record_delimiter}
("entity"{tuple_delimiter}"Tuning Parameters"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"Settings that adjust the response of a control loop (e.g., PID controller gains)."){record_delimiter}
("entity"{tuple_delimiter}"Alarm Limit"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"A threshold value that triggers an alarm when exceeded."){record_delimiter}
("entity"{tuple_delimiter}"Interlock Limit"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"A threshold value that triggers an automated safety action (interlock)."){record_delimiter}
("entity"{tuple_delimiter}"Size"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The physical dimensions of a device, such as valve size."){record_delimiter}
("entity"{tuple_delimiter}"Capacity"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The maximum flow rate or throughput a device can handle."){record_delimiter}
("entity"{tuple_delimiter}"Characteristics"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The relationship between valve position and flow rate (e.g., linear, equal percentage)."){record_delimiter}
("entity"{tuple_delimiter}"Metallurgy"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The specific metal composition and properties of a component."){record_delimiter}
("relationship"{tuple_delimiter}"Management of Change"{tuple_delimiter}"Instrumentation"{tuple_delimiter}"Changes to instrumentation that are not like-for-like require management through the MoC process."{tuple_delimiter}"process requirement, discipline involvement"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control Valve"{tuple_delimiter}"Size"{tuple_delimiter}"Changing the size of a control valve (e.g., 4\" to 6\") is a 'Not In-Kind' change requiring MoC."{tuple_delimiter}"modification type, parameter change"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"SIS Equipment"{tuple_delimiter}"Functionality"{tuple_delimiter}"Any change in the functionality of Safety Instrumented System (SIS) equipment requires MoC."{tuple_delimiter}"safety system, functional change"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"instrumentation, management of change, process control, SIS, equipment parameters, not in-kind, modification"){completion_delimiter}
#############################""",
    """Example 4:

Entity_types: [Equipment Tag, Equipment Type, Equipment Purpose, Hazard, Process, Engineering Discipline, Equipment Parameter]
Text:
```
| Tag No.         | Service location | Reason for relief | Set pressure barg | Accumulation % | Valve type | Discharge location | Remarks                                 |
|-----------------|------------------|-------------------|-------------------|----------------|------------|--------------------|-----------------------------------------|
| 150-RV-1001A/B  | C-15002          | (A)               | 22.0              | 10             | Pilot      | FDH                | GOVERNING. 140-LCV-1004 A/B fully open. |
| 150-RV-1001A/B  | E-15003          | (A)               | 22.0              | 10             | Pilot      | FDH                |                                         |
| 150-RV-1005A/B  | C-15003 E-15005  | (G)               | 14.5              | 10             | Balanced   | FDH                | GOVERNING                               |
| 150-RV-1005A/B  | C-15003 E-15005  | (D)               | 14.5              | 21             | Balanced   | FDH                | Fire surrounding C-15003                |


NOTES:
(A) Control valve failure
(D) External fire
(G) Loss of cooling duty
FDH = HP dry flare
```

Output:
("entity"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Relief valve 150-RV-1001A/B protecting equipment C-15002 and E-15003. Governing relief case is Control Valve Failure (A)."){record_delimiter}
("entity"{tuple_delimiter}"C-15002"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Equipment protected by relief valve 150-RV-1001A/B."){record_delimiter}
("entity"{tuple_delimiter}"E-15003"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Equipment protected by relief valve 150-RV-1001A/B."){record_delimiter}
("entity"{tuple_delimiter}"Set Pressure"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The pressure at which a relief valve is set to open."){record_delimiter}
("entity"{tuple_delimiter}"Accumulation %"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The percentage overpressure allowed during relief."){record_delimiter}
("entity"{tuple_delimiter}"Valve Type"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The design type of the relief valve (e.g., Pilot, Balanced)."){record_delimiter}
("entity"{tuple_delimiter}"Discharge Location"{tuple_delimiter}"Equipment Parameter"{tuple_delimiter}"The system where the relief valve discharges (e.g., FDH)."){record_delimiter}
("entity"{tuple_delimiter}"Control Valve Failure"{tuple_delimiter}"Process"{tuple_delimiter}"Relief case (A) caused by control valve failure."){record_delimiter}
("entity"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Relief valve 150-RV-1005A/B protecting equipment C-15003 and E-15005. Governing relief case is Loss of Cooling Duty (G)."){record_delimiter}
("entity"{tuple_delimiter}"C-15003"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Equipment protected by relief valve 150-RV-1005A/B."){record_delimiter}
("entity"{tuple_delimiter}"E-15005"{tuple_delimiter}"Equipment Tag"{tuple_delimiter}"Equipment protected by relief valve 150-RV-1005A/B."){record_delimiter}
("entity"{tuple_delimiter}"Loss of Cooling Duty"{tuple_delimiter}"Process"{tuple_delimiter}"Relief case (G) caused by loss of cooling duty."){record_delimiter}
("entity"{tuple_delimiter}"External Fire"{tuple_delimiter}"Hazard"{tuple_delimiter}"Relief case (D) caused by external fire."){record_delimiter}
("entity"{tuple_delimiter}"HP Dry Flare"{tuple_delimiter}"Equipment Type"{tuple_delimiter}"High Pressure Dry Flare system, destination for FDH discharge."){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"C-15002"{tuple_delimiter}"Relief valve 150-RV-1001A/B protects equipment C-15002."{tuple_delimiter}"protection, safety"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"E-15003"{tuple_delimiter}"Relief valve 150-RV-1001A/B protects equipment E-15003."{tuple_delimiter}"protection, safety"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Set Pressure"{tuple_delimiter}"Set Pressure for 150-RV-1001A/B is 22.0 barg."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Accumulation %"{tuple_delimiter}"Accumulation % for 150-RV-1001A/B is 10%."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Valve Type"{tuple_delimiter}"Valve Type for 150-RV-1001A/B is Pilot."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Discharge Location"{tuple_delimiter}"Discharge Location for 150-RV-1001A/B is FDH (HP Dry Flare)."{tuple_delimiter}"parameter value, destination"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1001A/B"{tuple_delimiter}"Control Valve Failure"{tuple_delimiter}"Control Valve Failure (A) is the GOVERNING relief case for 150-RV-1001A/B."{tuple_delimiter}"governing case, relief scenario, cause"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"C-15003"{tuple_delimiter}"Relief valve 150-RV-1005A/B protects equipment C-15003."{tuple_delimiter}"protection, safety"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"E-15005"{tuple_delimiter}"Relief valve 150-RV-1005A/B protects equipment E-15005."{tuple_delimiter}"protection, safety"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Set Pressure"{tuple_delimiter}"Set Pressure for 150-RV-1005A/B is 14.5 barg."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Accumulation %"{tuple_delimiter}"Accumulation % for 150-RV-1005A/B is 10% (governing case) or 21% (fire case)."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Valve Type"{tuple_delimiter}"Valve Type for 150-RV-1005A/B is Balanced."{tuple_delimiter}"parameter value, specification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Discharge Location"{tuple_delimiter}"Discharge Location for 150-RV-1005A/B is FDH (HP Dry Flare)."{tuple_delimiter}"parameter value, destination"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"Loss of Cooling Duty"{tuple_delimiter}"Loss of Cooling Duty (G) is the GOVERNING relief case for 150-RV-1005A/B."{tuple_delimiter}"governing case, relief scenario, cause"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"150-RV-1005A/B"{tuple_delimiter}"External Fire"{tuple_delimiter}"External Fire (D) is a non-governing relief case for 150-RV-1005A/B."{tuple_delimiter}"relief scenario, cause"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"relief valve, parameters, set pressure, accumulation, valve type, discharge location, relief case, governing case, control valve failure, loss of cooling duty, external fire, equipment protection"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction. Please find only the missing entities and relationships from previous text.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name
- entity_type: One of the following types: [{entity_types}]
- entity_description: Provide a comprehensive description of the entity's attributes and activities *based solely on the information present in the input text*. **Do not infer or hallucinate information not explicitly stated.** If the text provides insufficient information to create a comprehensive description, state "Description not available in text."
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add new entities and relations below using the same format, and do not include entities and relations that have been previously extracted. :\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Additional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

######################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be in JSON format, with no other text before and after the JSON. Use the same language as `Current Query`.

Output:
"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"

Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}

""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"

Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}

""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"

Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}

""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
