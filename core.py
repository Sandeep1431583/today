import json
import numpy as np
from src.backend.prompts import system_prompt , User_prompt
from src.backend.data import expected_output_format
from src.backend.output_format import ExpectedOutputFormat
from langchain.output_parsers import PydanticOutputParser


class Core:

    def dataprocessing(df, layout, FHIR_Resource, df_tc, df_ip, chglog):
        # Convert the DataFrame to a list of dictionaries

        # Convert NaN to None
        df = df.replace({np.nan: None})

        # Convert to JSON format
        json_data = {"instances": df.to_dict(orient='records')}
        
        # Convert the list of dictionaries to JSON format
        
        json_result = json.dumps(json_data, indent=4)
        json_result = json.loads(json_result)   
        print(json_result)

        if df_tc is not None:
            resulttc = df_tc.to_dict(orient='records')
        else:
            resulttc = []  # Assign an empty list
        
        if df_ip is not None:
            resultip = df_ip.to_dict(orient='records')
        else:
            resultip = []  # Assign an empty list

        json_result_tc = json.dumps(resulttc, indent=4)
        json_result_tc = json.loads(json_result_tc)   
        
        json_result_ip = json.dumps(resultip, indent=4)
        json_result_ip = json.loads(json_result_ip) 

        # Format the system prompt with the selected requirements
        formatted_sys_prompt = system_prompt.format(
            layout=layout,
            FHIR_Resource=FHIR_Resource
        )

        # formatted_expected_output_format = json.dumps(expected_output_format)
        myparser = PydanticOutputParser(pydantic_object=ExpectedOutputFormat)
        formatted_expected_output_format = myparser.get_format_instructions()

        formatted_user_prompt = User_prompt.format(
            mapping_json_template=json_result,
            layout=layout,
            FHIR_Resource=FHIR_Resource,
            test_case_csv=json_result_tc,
            sample_HL7=json_result_ip,
            chglog_1=chglog,
            expected_sample_output_format = formatted_expected_output_format
        )

        return formatted_sys_prompt , formatted_user_prompt
