export const useSearchFocus = () => {
    const searchInput = useState("searchInput", () => null);

    const focusSearch = () => {
        if (searchInput.value) {
            searchInput.value.focus();
        }
    };

    return {
        searchInput,
        focusSearch,
    };
};
