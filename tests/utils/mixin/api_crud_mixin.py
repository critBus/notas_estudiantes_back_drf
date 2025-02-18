import json
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from rest_framework import status

T = TypeVar("T")


class ApiCrudMixin:
    def call_create(
        self,
        url: str,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
        format_json=False,
    ) -> Optional[Dict[str, Any]]:
        if format_json:
            response = self.client.post(url, payload, format="json")
        else:
            response = self.client.post(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_update(
        self,
        url: str,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
        format_json=False,
    ) -> Optional[Dict[str, Any]]:
        if format_json:
            response = self.client.put(url, payload, format="json")
        else:
            response = self.client.put(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return None
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return None
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return None
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return None
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_partial_update(
        self,
        url: str,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
        format_json=False,
    ) -> Optional[Dict[str, Any]]:
        if format_json:
            response = self.client.patch(url, payload, format="json")
        else:
            response = self.client.patch(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return None
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return None
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return None
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return None
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_retrieve(
        self,
        url: str,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Dict:
        response = self.client.get(url)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_delete(
        self,
        url: str,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> None:
        response = self.client.delete(url)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def call_get(
        self,
        url: str,
        page: int = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[List[Dict[str, Any]]]:
        if page is not None:
            url = f"{url}?page={page}"
        response = self.client.get(url)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_get_list(
        self,
        url: str,
        schema_validator: Callable[[Dict], None],
        len_list: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[List[Dict[str, Any]]]:
        response_dict = self.call_get(
            url=url,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        if not (unauthorized or forbidden or bad_request or not_found):
            self.assertIsInstance(response_dict, list)
            self.assertEqual(len_list, len(response_dict))
            for result in response_dict:
                self.assertIsInstance(result, dict)
                schema_validator(result)

        return response_dict

    def call_list(
        self,
        url: str,
        len_list: int,
        schema_validator: Callable[[Dict], None] = None,
        total_count: int = None,
        expected_next: bool = False,
        expected_previous: bool = False,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[List[Dict[str, Any]]] | None:
        response_dict = self.call_get(
            url=url,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

        if not (unauthorized or forbidden or bad_request or not_found):
            if not total_count:
                total_count = len_list
            self.assertKey(
                response_dict=response_dict, key="meta", expected_type=dict
            )
            data = response_dict["meta"]
            self.assertKey(
                response_dict=data, key="count", expected=total_count
            )
            self.assertKey(
                response_dict=data,
                key="next",
                expected_none=not expected_next,
            )
            self.assertKey(
                response_dict=data,
                key="previous",
                expected_none=not expected_previous,
            )
            self.assertEqual(True, "result" in response_dict)
            results = response_dict["result"]
            self.assertIsInstance(results, list)
            self.assertEqual(len_list, len(results))
            if schema_validator:
                for result in results:
                    self.assertIsInstance(result, dict)
                    schema_validator(result)
            return results

        return response_dict

    def call_post(
        self,
        url: str,
        payload: Dict[str, Any],
        page: int = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
        format_json=False,
    ) -> Optional[Dict[str, Any]]:
        if page is not None:
            url = f"{url}?page={page}"
        if format_json:
            response = self.client.post(url, payload, format="json")
        else:
            response = self.client.post(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def assertKey(
        self,
        response_dict: Dict[str, Any],
        key: str,
        expected: Optional[T] = None,
        expected_any: Optional[List[T]] = None,
        expected_type: Optional[T] = None,
        expected_none: bool = False,
        expected_in_list_of_type: Optional[List[Type]] = None,
        expected_dict: Optional[Dict[str, Any]] = None,
        expected_subset: Optional[Dict[str, Any]] = None,
        expected_sub_list: Optional[List[Type]] = None,
    ) -> T:
        if key not in response_dict:
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
            print(f"key {key}")
        self.assertTrue(isinstance(response_dict, dict))
        self.assertEqual(True, key in response_dict)
        value: T = response_dict[key]
        if expected is not None:
            self.assertEqual(value, expected)
        elif expected_any is not None:
            self.assertEqual(True, value in expected_any)
        elif expected_in_list_of_type is not None:
            self.assertEqual(True, isinstance(value, list))
            self.assertEqual(len(expected_in_list_of_type), len(value))
            for i, element in enumerate(value):
                self.assertEqual(
                    True, isinstance(element, expected_in_list_of_type[i])
                )
        elif expected_type:
            self.assertEqual(True, isinstance(value, expected_type))
        elif expected_dict:
            self.assertEqual(True, isinstance(value, dict))
            self.assertDictEqual(value, expected_dict)
        elif expected_subset:
            self.assertEqual(True, isinstance(value, dict))
            self.assertDictContainsSubset(
                subset=expected_subset, dictionary=value
            )
        elif expected_sub_list:
            self.assertEqual(True, isinstance(value, list))
            for item in expected_sub_list:
                self.assertIn(member=item, container=value)
        else:
            self.assertEqual(expected_none, value is None)
        return value
