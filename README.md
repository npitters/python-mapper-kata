# python-mapper-kata

## The Scenario
Papillion Lavista High School (PLVHS) would like to upload statistics about their
Track & Field ahtletes to the National Track & Field Database (NTFDB).  The PLVHS
event statistics are stored in json files, the data for each file needs to be
translated to the format that the NTFDB requires.

## Prerequisites
[Poetry](https://python-poetry.org/docs/#installation)\
[Make](https://www.gnu.org/software/make/manual/make.html)

## The Challenge
An application has been stubbed out in the [app](app) directory and tests in the [tests](tests)
directory.  Using your TDD skills complete the `transform` function in the [transformer.py](app/transformer.py) module so that
it can receive the PLVHS json data and transform it into json that the NTFDB expects.
Examples of PLVHS input data can be found in the [example_input](example_input) directory.  The mapping rules for
the NTFDB data is defined in the [mapping definition](#mapping-definition) section below, all of these rules should be accounted for.

To run unit tests:  `make unit_tests`\
To execute the application:  `make run file=example_input/example_field.json` (use any json file you want)

### Mapping Definition
The following table defines all of the fields to be included in the NTFDB json data, the field that the
data comes from in the PLVHS json data (if applicable) and any rules to apply to execute the mapping.

**Note**:  Any required field that is either not included in the PLVHS data or is include but the
value is null should result in an exception being raised.

**Note**:  For any fields that require a translation, if a translation cannot be completed because
the value is not included in the translation table then an execption should be raised.

| NTFB Field (target) | Data Type | Required | PLVHS Field (source) | Rules                                                                      |
|---------------------| --------- |:--------:|--------------------- |----------------------------------------------------------------------------|
| id                  | string    |     X    | id                   |                                                                            |
| firstName           | string    |          | name                 | The `name` in the sourcde data is in the format `first name + ' ' + last name`.<br /><br />Map the `first name` part of of the source field.  If for some reason the `first name` cannot be parsed out then leave it out of the target json. |
| lastName            | string    |          | name                 | The `name` in the source data is in the format `first name + ' ' + last name`.<br /><br />Map the `last name` part of of the source field.  If for some reason the `last name` cannot be parsed out set this to the default value of "Unknown". |
| school              | string    |     X    |                      | Always map hard coded value "Papillion Lavistia High School"                |
| state               | string    |     X    |                      | Always map hard coded value "NE"                                            |
| grade               | int       |     X    | class                | The `grade` should be mapped based on the [Grade Mapping](#grade-mapping) translation table. |
| classification      | string    |     X    | eventClassification  | The `classification` should be mapped based on the [Classification Mapping](#classification-mapping) translation table. |
| eventName           | string    |     X    | eventId              | The `eventName` should be mapped based on the [Event Name Mapping](#event-name-mapping) translation table. |
| personalBest        | string    |          | times **or** marks   | If the source `eventTypeId == 1` (track) then this value is mapped from the `times` field.  If `eventTypeId == 2` (field) then this is mapped from the `marks` field.  Each of these are pipe delimited values.<br /><br />If mapping from the `times` field then select the **lowest** time from the list.  If mapping from the `marks` field then select the **highest** mark from the list.<br /><br />Additionaly, if mapping from the `marks` field the format of the values need to be translated.  In the source data the format is ***x*ft *y*in**, in the target data they need to be represted as ***x*' *y*"**.<br /><br />If source value not present or is null then target value should be null|
|topThree             | [string]  |     X    | times **or** marks   | If the source `eventTypeId == 1` (track) then this value is mapped from the `times` field.  If `eventTypeId == 2` (field) then this is mapped from the `marks` field.  Each of these are pipe delimited values.<br /><br />The target value is an array of 3 elements, and it always must be 3 elements.  If mapping from `times` then it should be the 3 **lowest** times, if mapping from `marks` it should be the 3 **highest** marks.  If 3 `times` or `marks` are not available then the array should be padded with null elements.<br /><br />The same rules for translating the format of `marks` applies. |

### Grade Mapping
| Source Value | Target Value |
| ------------ | ------------ |
| Freshman     | 9            |
| Sophomore    | 10           |
| Junior       | 11           |
| Senior       | 12           |

### Classification Mapping
| Source Value | Target Value |
| ------------ | ------------ |
| G            | Girls        |
| B            | Boys         |

### Event Name Mapping
| Source Value | Target Value |
| ------------ | ------------ |
| 1001         | 100m         |
| 1002         | 200m         |
| 1003         | 400m         |
| 1004         | 800m         |
| 1005         | 1600m        |
| 1006         | 3200m        |
| 2001         | Long Jump    |
| 2002         | Triple Jump  |
| 2003         | Pole Vault   |
| 2004         | High Jump    |
| 2005         | Shot Put     |
| 2006         | Discus       |
